"""Unified Newton-stratum API matches the layer predicates."""

from __future__ import annotations

from research.residuals.cubic_fibres import prefixes_at, same_depth_n2
from research.residuals.cubic_n0_reduction import n0_scaled
from research.residuals.cubic_n1_valuation import n1_after_n2, n21_agree
from research.residuals.stratum import (
    newton_stratum,
    newton_stratum_n0,
    newton_stratum_n1,
    newton_stratum_n2,
    newton_stratum_n21,
    newton_stratum_q,
)


def test_stratum_parameters_deficit_two():
    rec = newton_stratum(9, 2)
    assert rec["m"] == 6
    assert rec["exhausted"] is True
    assert rec["q_params"] == (0, 9, 4)


def test_stratum_n2_matches_visibility():
    k, r, m = 6, 1, 4
    for p in prefixes_at(m):
        for q in prefixes_at(m):
            assert newton_stratum_n2(p, q, k, r) == same_depth_n2(m, p, q, k)
            assert newton_stratum_n2(p, q, k, r) == ((p - q) % 3 == 0)


def test_stratum_n1_and_n21():
    k, r = 6, 1
    assert newton_stratum_n1(0, 3, k, r) == n1_after_n2(0, 3, k, r)
    assert newton_stratum_n21(0, 0, k, r) is True
    assert newton_stratum_n21(0, 1, k, r) == n21_agree(0, 1, k, r)


def test_stratum_n0_matches_scaling():
    assert newton_stratum_n0(1, 9, 2) == n0_scaled(1, 9, 2)
    assert newton_stratum_q(1, 9, 2) == n0_scaled(1, 9, 2)
