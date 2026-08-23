"""Milestone 14 counterexamples remain permanent regressions."""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.normalization import rewrite_sum
from bt.normtheory.calculus_link import D_coeff, D_normalize_words_equal
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.graph import distance_to_normal_form, geodesic_equals_excess
from bt.normtheory.hatd import hatD, hatD_raw, milestone14_witness, naive_raw_fails
from bt.normtheory.rewrite import weighted_l1_increases_on_two
from bt.normtheory.strategies import all_strategies, normal_form


def test_m14_witness_two_naive_drop():
    w = milestone14_witness()
    assert w.coeffs == (2,)
    nf = normal_form(w)
    assert nf.coeffs == (-1, 1)
    assert nf.value() == 2
    assert D(nf.value()) == 1
    assert D_coeff(w).coeffs == (0,)
    assert D_coeff(w).value() == 0
    assert not D_normalize_words_equal(w)
    assert naive_raw_fails(w)
    assert D(normal_form(w).value()) != D_coeff(w).value()


def test_m14_weighted_l1():
    assert weighted_l1_increases_on_two()


def test_m14_geodesic_five():
    five = CoeffWord((5,))
    assert geodesic_equals_excess(five) is False
    assert five.excess() == 4
    assert distance_to_normal_form(five) == 2


def test_m14_ab_count_gap():
    traces = all_strategies(CoeffWord((2, -2)))
    assert traces["A"].result.coeffs == traces["B"].result.coeffs
    assert traces["A"].rewrite_count != traces["B"].rewrite_count


def test_m14_parallel_depth_witness():
    traces = all_strategies(CoeffWord((-2, -2, 2)))
    assert traces["C"].passes > traces["A"].rewrite_count


def test_m14_rewrite_sum_five():
    assert rewrite_sum(5) == (2, 1)
    assert 2 not in (-1, 0, 1)
