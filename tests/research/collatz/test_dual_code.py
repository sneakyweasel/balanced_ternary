"""Exact dual valuation/lift coding."""

from __future__ import annotations

from itertools import product

from bt.representation import decode
from research.collatz.cylinders import belongs_to_cylinder
from research.collatz.dual_code import (
    CollatzDualCode,
    canonical_endpoint_formula,
    canonical_realizer_formula,
    decode_lift_digits,
    endpoint_successor,
    lift_digit_formula,
    lift_digit_from_state,
    reconstruct_realizer,
    valid_pair_word,
    verify_dual_exhaustive,
)
from research.collatz.itinerary import ValuationItinerary, verify_affine_against_T
from research.collatz.min_realizer import min_realizer


def test_benchmarks():
    ones = CollatzDualCode.from_valuations((1, 1, 1, 1))
    assert ones.lift_digits == (1, 1, 1, 1)
    assert ones.R == 31
    assert ones.realizers == (1, 3, 7, 15, 31)

    twos = CollatzDualCode.from_valuations((2, 2, 2, 2))
    assert twos.lift_digits == (0, 0, 0, 0)
    assert twos.R == 1


def test_direct_R_and_lift_formula_exhaustive_short():
    for m in range(6):
        words = ((),) if m == 0 else product(range(1, 5), repeat=m)
        for ks in words:
            ks = tuple(ks)
            dual = CollatzDualCode.from_valuations(ks)
            assert canonical_realizer_formula(ks) == min_realizer(ks)
            assert dual.R == min_realizer(ks)
            assert dual.validates()
            assert decode(dual.balanced_ternary_R) == dual.R
            assert belongs_to_cylinder(dual.R, ks)
            assert verify_affine_against_T(dual.R, ks)


def test_each_step_recurrence_and_bounds():
    for ks in product(range(1, 5), repeat=5):
        dual = CollatzDualCode.from_valuations(ks)
        for step in dual.steps:
            assert 0 <= step.lift_digit < (1 << step.valuation)
            assert step.R_after == step.R_before + (
                step.lift_digit << (step.K_before + 1)
            )
            assert (
                lift_digit_from_state(
                    step.index, step.endpoint_before, step.valuation
                )
                == step.lift_digit
            )
            assert (
                endpoint_successor(
                    step.index,
                    step.endpoint_before,
                    step.valuation,
                    step.lift_digit,
                )
                == step.endpoint_after
            )


def test_mixed_radix_reconstruction_and_uniqueness():
    ks = (1, 4, 2, 3, 1)
    dual = CollatzDualCode.from_valuations(ks)
    assert reconstruct_realizer(ks, dual.lift_digits) == dual.R
    assert decode_lift_digits(ks, dual.R) == dual.lift_digits
    assert valid_pair_word(ks, dual.lift_digits)
    wrong = list(dual.lift_digits)
    wrong[-1] = (wrong[-1] + 1) % (1 << ks[-1])
    assert not valid_pair_word(ks, wrong)


def test_formula_uses_affine_endpoint_not_trajectory_replay():
    parent = (1, 2, 3)
    it = ValuationItinerary.from_ks(parent)
    r = canonical_realizer_formula(parent)
    x = canonical_endpoint_formula(parent, r)
    assert x == it.apply(r)
    for k in range(1, 8):
        assert lift_digit_formula(parent, k) == lift_digit_from_state(
            len(parent), x, k
        )


def test_full_balanced_ternary_R_does_not_determine_successor_or_lift():
    a = CollatzDualCode.from_valuations((1,))
    b = CollatzDualCode.from_valuations((1, 4))
    assert a.R == b.R == 3
    assert a.balanced_ternary_R == b.balanced_ternary_R == "+0"
    assert a.endpoints[-1] == 5
    assert b.endpoints[-1] == 1
    assert lift_digit_formula((1,), 2) == 2
    assert lift_digit_formula((1, 4), 2) == 0


def test_streaming_exhaustive_through_m8_k5():
    assert verify_dual_exhaustive(max_length=8, k_max=5) == 488_281
