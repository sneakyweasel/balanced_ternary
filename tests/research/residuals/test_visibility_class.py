"""Visibility class of a general integer polynomial."""

from __future__ import annotations

from itertools import product

from bt.calculus.residual import TRITS
from bt.calculus.section import parse_poly
from research.residuals.add_residual import step_carry, sum_residual_identity
from research.residuals.visibility_class import (
    class_report,
    formula_matches_residual_along,
    has_visibility,
    predicts_visibility,
)


SAMPLES = (
    parse_poly("x^2"),
    parse_poly("x^3"),
    parse_poly("x^4"),
    parse_poly("x^3-x"),
    parse_poly("x^2+x^3"),
    parse_poly("3x^2"),
    parse_poly("x^5"),
    parse_poly("2x+1"),
)


def test_closed_form_matches_residual_along():
    for f in SAMPLES:
        assert formula_matches_residual_along(f, max_m=3)


def test_named_visibility_at_deficit_one():
    k, r = 5, 1
    assert predicts_visibility(parse_poly("x^3"), k, r) is True
    assert has_visibility(parse_poly("x^3"), k, r) is True
    assert predicts_visibility(parse_poly("x^3-x"), k, r) is True
    assert has_visibility(parse_poly("x^3-x"), k, r) is True
    assert predicts_visibility(parse_poly("x^2+x^3"), k, r) is True
    assert has_visibility(parse_poly("x^2+x^3"), k, r) is True
    assert predicts_visibility(parse_poly("x^2"), k, r) is False
    assert has_visibility(parse_poly("x^2"), k, r) is False
    assert predicts_visibility(parse_poly("x^4"), k, r) is False
    assert has_visibility(parse_poly("x^4"), k, r) is False
    assert predicts_visibility(parse_poly("2x+1"), k, r) is False
    assert has_visibility(parse_poly("2x+1"), k, r) is False


def test_degree_four_and_five_break_the_cubic_unit_law():
    k, r = 5, 1
    assert predicts_visibility(parse_poly("x^3+x^4"), k, r) is True
    assert has_visibility(parse_poly("x^3+x^4"), k, r) is False
    assert predicts_visibility(parse_poly("x^5"), k, r) is False
    assert has_visibility(parse_poly("x^5"), k, r) is True


def test_sum_residual_is_constant_carry():
    f = parse_poly("x^3")
    g = parse_poly("x^2+1")
    assert step_carry(f, g, 1) in (-1, 0, 1)
    for m in range(4):
        for word in product(TRITS, repeat=m):
            assert sum_residual_identity(f, g, word)


def test_visibility_predicate_degree_three():
    for k in (4, 5):
        report = class_report(k=k, r=1, max_degree=3)
        assert report["mismatch_count"] == 0
        assert report["actual_true"] == 4 * 5**3
