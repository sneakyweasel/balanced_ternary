"""First intermediate cubic layer: depth deficit 1 (m = k-2)."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

import pytest

from balanced_ternary.cli import main
from bt.calculus.cubic import F_k
from research.residuals.cubic_deepest import deepest_class_count
from research.residuals.cubic_fibres import C_km, prefixes_at
from research.residuals.cubic_layer import (
    inter_class_count,
    inter_equiv,
    inter_n0,
    inter_n1,
    inter_n1_agree,
    inter_n2,
    inter_n2_agree,
    inter_zero_fibre,
    layer_depth,
    layer_report,
    n21_image,
    n2_image,
    one_layer_surplus,
    zero_exp_inter,
)
from bt.calculus.quadratic import iter_dz


def test_newton_simplification():
    for k in range(3, 9):
        mod = 3**k
        m = k - 2
        for p in prefixes_at(m):
            N0, N1, N2, N3 = F_k(m, p, k)
            assert N3 % mod == 0
            assert N2 % mod == (2 * 3 ** (k - 1) * p) % mod
            assert inter_n2(p, k) == N2 % mod
            assert inter_n0(p, k) == iter_dz(p**3, m) % mod
            if k >= 4:
                assert N1 % mod == (3 * p * p + 3 ** (k - 1) * p) % mod
                assert inter_n1(p, k) == N1 % mod


def test_fibre_criterion_matches_F_k():
    for k in range(3, 8):
        ps = list(prefixes_at(k - 2))
        for i, p in enumerate(ps):
            for q in ps[i:]:
                assert inter_equiv(p, q, k) == (F_k(k - 2, p, k) == F_k(k - 2, q, k))


def test_n2_has_three_classes():
    for k in range(3, 10):
        assert len(n2_image(k)) == 3


def test_n21_strictly_refines_to_full():
    for k in range(4, 9):
        n21 = len(n21_image(k))
        full = inter_class_count(k)
        assert n21 < full
        assert 3 < n21


def test_known_intermediate_counts():
    table = {
        3: 3,
        4: 9,
        5: 27,
        6: 80,
        7: 240,
        8: 721,
        9: 2178,
        10: 6537,
    }
    for k, C in table.items():
        assert inter_class_count(k) == C
        assert C_km(k, k - 2) == C


@pytest.mark.slow
def test_known_intermediate_counts_high_k():
    table = {
        11: 19652,
        12: 58977,
        13: 177057,
        14: 531230,
    }
    for k, C in table.items():
        assert inter_class_count(k) == C
        assert C_km(k, k - 2) == C


def test_surplus_table():
    deltas = {
        4: 1,
        5: 3,
        6: 4,
        7: 8,
        8: 5,
        9: 25,
        10: 16,
    }
    for k, d in deltas.items():
        assert one_layer_surplus(k) == d


@pytest.mark.slow
def test_surplus_table_high_k():
    deltas = {
        11: 55,
        12: 38,
        13: 149,
        14: 89,
    }
    for k, d in deltas.items():
        assert one_layer_surplus(k) == d


def test_unit_sign_pairs_split():
    for k in range(4, 9):
        assert inter_n2_agree(1, -1, k) is False
        assert F_k(k - 2, 1, k) != F_k(k - 2, -1, k)
        assert F_k(k - 2, 1, k - 1) == F_k(k - 2, -1, k - 1)


def test_sign_n2_iff_divisible_by_three():
    for k in range(3, 8):
        for p in prefixes_at(k - 2):
            assert inter_n2_agree(p, -p, k) == (p % 3 == 0)
            assert inter_n1_agree(p, -p, k) == (p % 3 == 0)


def test_zero_exponent_and_fibre():
    for k in range(3, 10):
        r = zero_exp_inter(k)
        assert r == (2 * k) // 3
        members = inter_zero_fibre(k)
        expected = [p for p in prefixes_at(k - 2) if p % (3**r) == 0]
        assert members == expected
        zero = F_k(k - 2, 0, k)
        assert all(F_k(k - 2, p, k) == zero for p in members)


def test_uncompressed_small_horizons():
    for k in (3, 4, 5):
        assert inter_class_count(k) == 3 ** (k - 2)


def test_no_naive_recurrence():
    assert inter_class_count(8) != deepest_class_count(7)
    assert inter_class_count(8) != 3 * C_km(7, 5)
    assert inter_class_count(8) == 721
    assert deepest_class_count(7) == 716


def test_layer_report_and_kinds():
    rec = layer_report(6)
    assert rec["k"] == 6
    assert rec["m"] == 4
    assert rec["raw"] == 81
    assert rec["N2"] == 3
    assert rec["C"] == 80
    assert rec["Delta"] == 4
    kinds = rec["kinds"]
    assert kinds["singleton"] == 79
    assert kinds["sign"] == 1


def test_cli_cubic_layer():
    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("cubic-layer", "--k", "6", "--depth-deficit", "1")
    assert "m = 4" in out
    assert "N2 classes = 3" in out
    assert "C(k,k-2) = 80" in out
    one = _run("cubic-layer-fibre", "3", "--k", "6", "--depth-deficit", "1")
    assert "fibre_size = 2" in one
    assert " -3" in one or "-3" in one
    assert "3" in one


def test_layer_depth_rejects_other_deficits():
    assert layer_depth(8, 1) == 6
    try:
        layer_depth(8, 2)
    except ValueError:
        return
    raise AssertionError("deficit 2 should be rejected")
