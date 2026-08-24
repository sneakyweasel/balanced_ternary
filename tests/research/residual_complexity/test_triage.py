"""Phase-0 tests for unrestricted residual complexity C_F(m,r)."""

from __future__ import annotations

from bt.calculus.myhill_nerode import equiv_recursive, levelled_mealy_count
from bt.calculus.quadratic import invariant_mod, pack_word, quadratic_residual_formula
from bt.calculus.residual import residual_along
from research.regular_output_preimages.triage import census_count as safety_census_count
from research.residual_complexity.problem import PROBLEM
from research.residual_complexity.triage import (
    MAX_DEPTH,
    SAFETY_HORIZON7,
    X,
    X2,
    X2_CENSUS,
    census_count,
    census_count_mealy,
    census_count_quad,
    census_table,
    colliding_pairs_at,
    half_repunit,
    linear_is_constant_one,
    residuals_at,
    simple_formula_failures,
    squared_half_repunit_digits,
    superdiagonal_pairs,
    triage_report,
    type_cap,
    x2_proved_count,
)


def test_problem_is_registered():
    from research.open_problems import get_problem

    assert get_problem("residual_complexity") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/residual_complexity.md",)
    assert PROBLEM.id == "residual_complexity"


def test_identity_has_one_unrestricted_type():
    record = linear_is_constant_one(4)
    assert record["single_type"]
    assert record["clock_grows"]
    assert residuals_at(X, 3) == [X]
    assert census_count(X, 2, 3) == 1
    assert census_count(X, 4, 0) == 1
    assert levelled_mealy_count(X, 4) == 4


def test_identity_residual_is_itself():
    assert residual_along(X, (1, 0, -1, 1)).coeffs == X.coeffs


def test_mealy_signature_agrees_with_phi_on_small_depths():
    for m in range(4):
        for r in range(4):
            assert census_count(X2, m, r) == census_count_mealy(X2, m, r)
            assert census_count(X2, m, r) == census_count_quad(X2, m, r)
            assert census_count(X, m, r) == census_count_mealy(X, m, r)


def test_x2_layer_is_the_full_prefix_tree():
    for m in range(6):
        assert len(residuals_at(X2, m)) == 3**m


def test_proved_band_matches_census_through_seven():
    table = census_table(X2, MAX_DEPTH)
    assert table == X2_CENSUS
    for m in range(MAX_DEPTH + 1):
        for r in range(MAX_DEPTH + 1):
            proved = x2_proved_count(m, r)
            if proved is not None:
                assert table[m][r] == proved
            assert table[m][r] <= type_cap(m, r)
            assert table[m][r] <= 3**m


def test_squared_half_repunit_expansion_packs_and_digit_r_never_plus():
    for r in range(1, 9):
        digits = squared_half_repunit_digits(r)
        assert pack_word(digits) == half_repunit(r) ** 2
        assert digits[r] in (0, -1)
        assert 1 not in digits[r : r + 1]


def test_superdiagonal_pairs_are_exactly_the_three_constant_extensions():
    for m in range(2, 7):
        expected = set(superdiagonal_pairs(m))
        expected |= {(b, a) for a, b in expected}
        found = colliding_pairs_at(m, m - 1)
        assert len(found) == 3
        for left, right in found:
            assert (left, right) in expected or (right, left) in expected
            f = quadratic_residual_formula(left)
            g = quadratic_residual_formula(right)
            assert equiv_recursive(f, g, m - 1)
            assert invariant_mod(f, m - 1) == invariant_mod(g, m - 1)


def test_superdiagonal_formula_is_three_to_the_m_minus_three():
    for m in range(2, 8):
        assert census_count(X2, m, m - 1) == 3**m - 3
        assert x2_proved_count(m, m - 1) == 3**m - 3


def test_not_a_remaining_horizon_clock_or_safety_census():
    table = census_table(X2, 4)
    failures = simple_formula_failures(table)
    assert failures["not_three_min"]
    assert failures["not_coefficient_cap"]
    assert failures["witness_three_min"] == (2, 1, 6, 3)
    assert census_count(X2, 2, 1) == 6
    assert 3 ** min(2, 1) == 3
    assert SAFETY_HORIZON7 == (1, 3, 7, 16, 33, 66, 131, 260)
    unrestricted_h7 = tuple(X2_CENSUS[m][7] for m in range(8))
    assert unrestricted_h7 == (1, 3, 9, 27, 81, 243, 729, 2187)
    assert unrestricted_h7 != SAFETY_HORIZON7
    assert safety_census_count(X2, 2, 7) == 7
    assert safety_census_count(X2, 3, 7) == 16


def test_interior_is_not_claimed_by_the_band_formula():
    assert x2_proved_count(4, 2) is None
    assert X2_CENSUS[4][2] == 50
    assert x2_proved_count(5, 2) is None
    assert X2_CENSUS[5][2] == 77


def test_triage_report_shape():
    report = triage_report(3)
    assert report["polynomials"] == ["x", "x^2"]
    assert report["linear"]["single_type"]
    assert report["not_a_clock"]
    assert report["band_formula_holds"]
    assert report["formula_failures"]["not_three_min"]
    assert len(report["x2_census"]) == 4
    assert MAX_DEPTH == 7
    assert report["ahmed_savchuk_unrestricted_infinite"]
