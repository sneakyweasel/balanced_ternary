"""Phase-0 tests for balanced digit sums of nonlinear polynomial values."""

from __future__ import annotations

from itertools import product

import pytest

from bt.calculus.residual import TRITS, section_value
from bt.calculus.section import parse_poly
from bt.sequences import bt_digit_sum
from research.balanced_digit_sum_polynomials.problem import PROBLEM
from research.balanced_digit_sum_polynomials.triage import (
    FAST_DEPTH,
    MAX_DEPTH,
    ordinary_s3,
    ordinary_window_comparison,
    prefix_one_then_zeros,
    make_row,
    terminal_correction_holds,
    translation_holds,
    translation_s_bal,
    census_poly,
    triage_report,
)


def test_problem_is_registered():
    from research.literature import get_reference
    from research.open_problems import get_problem

    assert get_problem("balanced_digit_sum_polynomials") is PROBLEM
    assert PROBLEM.status == "EXPLORATORY"
    assert PROBLEM.docs == ("docs/problems/balanced_digit_sum_polynomials.md",)
    assert get_reference("oeis-A065363")["id"] == "oeis-A065363"
    assert get_reference("stoll-2012-digits-polynomial-ap")["year"] == 2012


def test_translation_identity_on_a_window():
    for n in range(-120, 121):
        assert translation_holds(n)
    assert translation_s_bal(5) == bt_digit_sum(5)
    assert ordinary_s3(5) == 3
    assert translation_s_bal(-7) == -translation_s_bal(7)


def test_terminal_correction_matches_direct_digit_sum():
    f = parse_poly("x^2")
    for word in product(TRITS, repeat=3):
        assert terminal_correction_holds(f, word)
        row = make_row("x^2", f, word)
        assert row.exact_sum == row.partial_sum + row.terminal
        assert row.packed == section_value(word)
        assert row.exact_sum == bt_digit_sum(f.eval(row.packed))


def test_prefix_zero_is_not_the_exact_integer_zero():
    """S_k=0 is not P(n)=0 and is not automatically s_bal(P(n))=0."""

    f = parse_poly("x^2")
    found = None
    for word in product(TRITS, repeat=3):
        row = make_row("x^2", f, word)
        if row.partial_sum == 0 and row.exact_sum != 0:
            found = row
            break
    assert found is not None
    assert f.eval(found.packed) != 0


def test_census_accounting_x2_small():
    rows = census_poly("x^2", parse_poly("x^2"), 3, sig_horizon=2)
    assert [row["raw_prefixes"] for row in rows] == [1, 3, 9, 27]
    prev_prefix = 1
    for row in rows:
        assert row["prefix_zeros"] <= row["raw_prefixes"]
        assert row["joint_states"] <= row["raw_prefixes"]
        assert row["residual_states"] <= row["raw_prefixes"]
        if row["depth"] == 0:
            assert row["stay_zero"] == row["leave_zero"] == row["enter_zero"] == 0
        else:
            assert row["stay_zero"] + row["leave_zero"] == 3 * prev_prefix
        prev_prefix = row["prefix_zeros"]


def test_ordinary_comparison_uses_the_translation():
    record = ordinary_window_comparison(parse_poly("x^2"), 4)
    assert record["exact_zeros"] == record["translation_zeros"]
    assert record["ordinary_s3_zeros"] <= record["exact_zeros"]


def test_triage_report_shape():
    report = triage_report(max_depth=3, sig_horizon=2, compare_depth=3)
    assert report["translation_identity"]
    assert report["terminal_correction"]
    assert set(report["census"]) == {"x^2", "x^3", "x^3-x", "x^4", "x^2+x"}
    assert report["x2_joint_grows"]
    assert report["monna_opened"] is False
    assert prefix_one_then_zeros(2) == (1, 0, 0)
    assert FAST_DEPTH == 4
    assert MAX_DEPTH == 10
    family = report["x2_prefix_family"]
    assert family["undistinguished_pairs"] == 0
    assert family["distinguished_pairs"]


@pytest.mark.slow
def test_phase0_census_through_depth_ten():
    report = triage_report(max_depth=MAX_DEPTH, sig_horizon=2, compare_depth=6)
    assert report["translation_identity"]
    x2 = report["census"]["x^2"]
    assert x2[-1]["depth"] == 10
    assert x2[-1]["raw_prefixes"] == 3**10
    assert x2[-1]["joint_states"] == 3**10
    assert x2[-1]["exact_zeros"] == 6495
    assert x2[-1]["prefix_zeros"] == 9495
    assert report["ordinary_comparison"]["x^2"]["exact_zeros"] == 55
    assert report["ordinary_comparison"]["x^2"]["ordinary_s3_zeros"] == 1
