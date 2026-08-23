"""Phase-0 tests for balanced-Monna endpoint pairs and cubic jump depths."""

from __future__ import annotations

from fractions import Fraction

from research.monna_endpoint_spectra.problem import PROBLEM
from research.monna_endpoint_spectra.triage import (
    MAX_N,
    PLUS_ONE,
    EndpointPair,
    X,
    X3,
    NEG_X,
    cubic_difference_formula,
    difference_is_four_pow,
    endpoint_normal_form,
    eval_poly,
    euclidean_jump,
    iterate_pairs,
    monna_value,
    pack_word,
    padic_divergence_depth,
    predicted_divergence_depth,
    predicted_spectrum_closed_form,
    preserves_pair,
    spectrum_counts,
    triage_report,
    v3_frac,
)


def test_problem_is_registered():
    from research.open_problems import get_problem

    assert get_problem("monna_endpoint_spectra") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/monna_endpoint_spectra.md",)


def test_half_has_constant_minus_digits():
    half = Fraction(1, 2)
    assert monna_value(half) == Fraction(-1, 2)
    assert monna_value(-half) == Fraction(1, 2)
    assert v3_frac(half) == 0


def test_constructed_pairs_collide_under_monna():
    pair = EndpointPair(2, (1, 0), "plus")
    u, v = pair.values()
    assert u - v == 4 * 9
    assert monna_value(u) == monna_value(v)
    assert monna_value(u) == pair.monna()
    assert difference_is_four_pow(pair)


def test_both_kinds_are_endpoint_pairs():
    for kind in ("plus", "minus"):
        pair = EndpointPair(1, (0,), kind)
        u, v = pair.values()
        assert monna_value(u) == monna_value(v)
        assert endpoint_normal_form(u, v)
        assert u != v


def test_normal_form_and_difference_on_the_full_n3_window():
    for pair in iterate_pairs(3):
        u, v = pair.values()
        assert difference_is_four_pow(pair)
        assert monna_value(u) == monna_value(v)
        assert endpoint_normal_form(u, v)
        assert pack_word(pair.prefix) == pair.pack


def test_cubic_difference_and_valuation_law():
    for n in range(4):
        for pair in iterate_pairs(n):
            u, v = pair.values()
            left = eval_poly(X3, u) - eval_poly(X3, v)
            assert left == cubic_difference_formula(pair)
            assert padic_divergence_depth(X3, pair) == predicted_divergence_depth(pair)


def test_identity_and_negation_preserve_endpoints():
    pair = EndpointPair(2, (-1, 1), "minus")
    assert preserves_pair(X, pair)
    assert preserves_pair(NEG_X, pair)
    assert euclidean_jump(X, pair) == 0
    assert euclidean_jump(NEG_X, pair) == 0


def test_x3_does_not_preserve_a_generic_pair():
    pair = EndpointPair(1, (1,), "plus")
    assert euclidean_jump(X3, pair) != 0
    u, v = pair.values()
    assert not endpoint_normal_form(eval_poly(X3, u), eval_poly(X3, v))


def test_spectrum_closed_form_matches_enumeration():
    for n in range(MAX_N + 1):
        assert spectrum_counts(n) == predicted_spectrum_closed_form(n)
    assert predicted_spectrum_closed_form(0) == {0: 2}
    assert predicted_spectrum_closed_form(1)[3] == 2


def test_x_plus_one_fails_exactly_on_all_plus_plus_kind():
    fails = []
    for n in range(MAX_N + 1):
        for pair in iterate_pairs(n):
            if not preserves_pair(PLUS_ONE, pair):
                fails.append(pair)
    assert [(p.n, p.kind, p.prefix) for p in fails] == [
        (n, "plus", (1,) * n) for n in range(MAX_N + 1)
    ]


def test_triage_report_shape():
    report = triage_report(2)
    assert report["difference_four"]
    assert report["monna_collision"]
    assert report["spectrum_formula_matches_enumeration"]
    assert report["x_preserves"]
    assert report["neg_x_preserves"]
    assert report["constants_preserve"]
    assert report["cubic"]["formula_fails"] == 0
    assert report["cubic"]["depth_mismatches"] == 0
    assert report["cubic"]["preservations"] == 0
