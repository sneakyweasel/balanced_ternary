"""Phase-0 visibility gate for same-depth fibres of x^4."""

from __future__ import annotations

from itertools import product

import pytest

from bt.calculus.cubic import prefixes_at
from bt.calculus.residual import TRITS, residual_along
from research.residuals.x4_stratum import (
    F_k,
    X4,
    leftover_matches,
    linear_coeff_valuation,
    n0_scaled_fourth,
    n2_square_residue,
    quartic_coeffs,
    quartic_residual_formula,
    triage_report,
    visibility_scan,
)


def test_closed_form_matches_residual_along():
    for m in range(5):
        for word in product(TRITS, repeat=m):
            assert quartic_residual_formula(word) == residual_along(X4, word)


def test_binomial_coeffs_at_small_words():
    A, B, C, D, E = quartic_coeffs(2, 1)
    assert A == 3**6
    assert B == 4 * 3**4
    assert C == 6 * 3**2
    assert D == 4
    assert E == 0


def test_linear_coeff_valuation_is_2m_on_units():
    for m in range(6):
        assert linear_coeff_valuation(m, 1) == 2 * m
        assert linear_coeff_valuation(m, -1) == 2 * m


def test_leftover_two_regime_identity():
    for m in range(6):
        for r in (0, 1):
            for p in prefixes_at(m):
                if r and p % 3:
                    continue
                assert leftover_matches(p, m, r)
                u = p // (3**r) if r else p
                assert n0_scaled_fourth(u, m, r) == quartic_coeffs(m, p)[4]


def test_visibility_verdict_k_le_5():
    report = triage_report(5)
    assert report["formula_matches_residual_along"] is True
    assert report["leftover_two_regime"] is True
    assert report["degree_increment_n3"] is False
    assert report["r1_has_visibility"] is False
    assert report["n2_sees_square"] is True
    assert report["verdict"] == "CLOSE"
    for row in report["rows"]:
        if row["r"] == 1 and row["k"] >= 4:
            assert row["visible_indices"] == []
            assert row["visibility"] == [False, False, False, False, False]
            assert row["constant"][3] is True
            assert row["constant"][4] is True
            assert row["sees_square"][2] is True


def test_n1_visibility_is_a_width_three_accident():
    rows = { (row["k"], row["r"]): row for row in visibility_scan(4) }
    assert rows[(3, 1)]["visible_indices"] == [1]
    assert rows[(4, 1)]["visible_indices"] == []


def test_n2_square_filter_at_deficit_one():
    for k in range(3, 6):
        m = k - 2
        for p in prefixes_at(m):
            assert F_k(m, p, k)[2] == n2_square_residue(p, k)


@pytest.mark.slow
def test_visibility_scan_k_le_7():
    rows = visibility_scan(7)
    r1 = [row for row in rows if row["r"] == 1 and row["k"] >= 4]
    assert r1
    assert all(row["visible_indices"] == [] for row in r1)
    assert all(row["leftover_two_regime"] for row in rows)
    assert all(row["sees_square"][2] for row in r1)
    for row in r1:
        m, k = row["m"], row["k"]
        for p in prefixes_at(m):
            n0, n1, n2, n3, n4 = F_k(m, p, k)
            assert n3 == 0
            assert n4 == 0
            assert n2 == n2_square_residue(p, k)
