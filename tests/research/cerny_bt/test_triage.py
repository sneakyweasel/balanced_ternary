"""Phase-0 tests for a transition-closed residual quotient."""

from __future__ import annotations

from bt.calculus.myhill_nerode import equiv_recursive
from bt.calculus.residual import TRITS, delta
from bt.calculus.section import parse_poly
from research.cerny_bt.problem import PROBLEM
from research.cerny_bt.triage import (
    AFFINE_SPECS,
    NONLINEAR_SPECS,
    affine_closure,
    affine_family_record,
    affine_intercept_bound,
    affine_step,
    approx_equals_raw_on_sample,
    approx_r,
    horizon_not_congruence_witness,
    nonlinear_family_record,
    observed_leading_coefficient,
    residual_closure,
    section_leading_coefficient,
    triage_report,
)


def test_closed_problem_is_registered():
    from research.open_problems import get_problem

    assert PROBLEM.status == "ARCHIVED"
    assert get_problem("cerny_bt") is PROBLEM


def test_horizon_relation_is_not_a_transition_congruence():
    witness = horizon_not_congruence_witness()
    left = parse_poly(str(witness["p"]))
    right = parse_poly(str(witness["q"]))
    assert witness["equiv_at_horizon"] is True
    assert equiv_recursive(left, right, 1)
    assert witness["D_p"] == "x"
    assert witness["D_q"] == "1 + x"
    assert witness["children_equiv_at_same_horizon"] is False
    assert witness["approx_r_on_prefixes"] is False
    assert witness["shortest_distinction"] == [-1, -1]


def test_approx_r_refines_horizon_equivalence_on_the_witness():
    left = parse_poly("x")
    right = parse_poly("x+3")
    assert equiv_recursive(left, right, 1)
    assert not approx_r(left, right, 1, prefix_bound=1)
    assert approx_r(left, left, 1, prefix_bound=2)


def test_affine_residuals_are_transition_closed_and_bounded():
    expected_counts = {
        "0": 1,
        "1": 2,
        "-1": 2,
        "2": 3,
        "x": 1,
        "x+1": 2,
        "x-1": 2,
        "2x+1": 3,
        "2x-1": 3,
        "-x": 1,
        "3x+1": 3,
        "-2x+1": 3,
    }
    for spec in AFFINE_SPECS:
        record = affine_family_record(spec)
        f = parse_poly(spec)
        slope, intercept = f.coefficient(1), f.coefficient(0)
        bound = affine_intercept_bound(slope, intercept)
        intercepts = affine_closure(slope, intercept)
        assert record["finite"]
        assert record["transition_closed"]
        assert record["state_count"] == expected_counts[spec]
        assert record["state_count"] == len(intercepts)
        assert max(abs(value) for value in intercepts) <= bound
        for value in intercepts:
            for trit in TRITS:
                assert affine_step(slope, value, trit) in intercepts


def test_nonlinear_leading_coefficients_are_unbounded():
    for spec in NONLINEAR_SPECS:
        record = nonlinear_family_record(spec)
        f = parse_poly(spec)
        assert record["finite"] is False
        assert record["distinct_leading_coefficients"]
        for depth in range(4):
            word = (0,) * depth
            formula = section_leading_coefficient(f, depth)
            assert formula == observed_leading_coefficient(f, word)
            assert formula == record["leading_formula"][depth]
            if depth >= 1:
                assert abs(formula) > abs(section_leading_coefficient(f, depth - 1))


def test_every_nonzero_leading_coefficient_grows_for_degree_at_least_two():
    for spec, word in (("x^2", (1, -1, 0)), ("x^3", (-1, 1, 1))):
        f = parse_poly(spec)
        for depth in range(1, 4):
            prefix = word[:depth]
            assert observed_leading_coefficient(f, prefix) == section_leading_coefficient(
                f, depth
            )


def test_approx_r_matches_raw_equality_on_affine_closures():
    assert approx_equals_raw_on_sample(r=1, prefix_bound=2)
    assert approx_equals_raw_on_sample(r=2, prefix_bound=1)


def test_horizon_zero_is_the_universal_relation():
    left = parse_poly("x^2")
    right = parse_poly("x^3")
    assert equiv_recursive(left, right, 0)
    assert approx_r(left, right, 0, prefix_bound=2)


def test_nonlinear_closure_is_not_completed_inside_the_cap():
    record = residual_closure(parse_poly("x^2"), max_states=16)
    assert record.truncated
    assert record.finite is False
    assert record.state_count is None


def test_gate_closes_as_reparameterization():
    report = triage_report()
    assert report["gate"] == "CLOSE"
    assert report["classification"] == "REPARAMETERIZATION"
    assert report["canonical_nonaffine_finite_quotient"] is False
    assert report["approx_equals_raw_on_sample"]
    assert all(row["finite"] for row in report["affine_families"])
    assert all(not row["finite"] for row in report["nonlinear_families"])
    assert {row["family"] for row in report["affine_families"]} == set(AFFINE_SPECS)


def test_every_trit_fails_to_preserve_the_horizon_witness():
    left = parse_poly("x")
    right = parse_poly("x+3")
    assert equiv_recursive(left, right, 1)
    assert all(
        not equiv_recursive(delta(left, trit), delta(right, trit), 1) for trit in TRITS
    )
