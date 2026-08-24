"""Exact image counts for the residual machine of x^3."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

import pytest

from bt.calculus.cubic import M_k_x3, prefixes_at, raw_count_x3
from cli.main import main
from research.residuals.cubic_fibres import C_km, balanced_bound
from research.residuals.cubic_deepest import deepest_class_count
from research.residuals.cubic_layer import inter_class_count
from research.residuals.x3_state_complexity import (
    A_coord,
    C_km_count,
    C_layer,
    C_unexhausted_formula,
    core_u_range,
    easy_count,
    g_poly,
    image_count_report,
    in_core_domain,
    joint_image_size,
    layer_count_report,
    M_k_count,
    overlaps_report,
    same_depth_total,
    square_modulus_exp,
    states_report,
    unit_g_injective_mod,
    unexhausted_zero_size,
    zero_spine_overcount,
)
from research.residuals.stratum import (
    newton_stratum_core_width,
    newton_stratum_n0_neg,
    newton_stratum_n1_square,
    newton_stratum_q_unit_family,
    newton_stratum_unit_square,
)


def test_easy_count_matches_enumeration():
    for m in range(0, 6):
        for r in range(0, m + 3):
            expected = sum(
                1
                for p in prefixes_at(m)
                if p != 0 and (p % (3**r) != 0 if r else True)
            )
            if r == 0:
                expected = 0
            elif r > m:
                expected = 3**m
            else:
                expected = sum(1 for p in prefixes_at(m) if p % (3**r) != 0)
            assert easy_count(m, r) == expected


def test_core_domain_iff():
    for m in range(0, 6):
        for r in range(0, m + 1):
            W = m - r
            for u in range(-((3 ** max(W, 0) - 1) // 2) - 3, (3 ** max(W, 0) - 1) // 2 + 4):
                left = abs((3**r) * u) <= balanced_bound(m)
                right = abs(u) <= balanced_bound(W)
                assert left == right
                assert in_core_domain(u, m + 1 + r, r) == right
                assert newton_stratum_core_width(m, r, u) == right


def test_C_matches_hash_through_k10():
    for k in range(1, 11):
        for m in range(k):
            assert C_km_count(k, m) == C_km(k, m)
            assert C_layer(k, k - 1 - m) == C_km(k, m)


def test_unexhausted_formula():
    for k in range(2, 12):
        for r in range(k):
            if k < 4 * r + 1 and r <= k - 1 - r:
                assert C_unexhausted_formula(k, r) == C_km(k, k - 1 - r)
                Z = unexhausted_zero_size(k, r)
                assert Z >= 1
                m = k - 1 - r
                assert C_km(k, m) == 3**m - Z + 1


def test_known_layer_counts():
    assert deepest_class_count(8) == C_layer(8, 0)
    assert inter_class_count(8) == C_layer(8, 1)


@pytest.mark.slow
def test_known_layer_counts_high_k():
    assert C_layer(14, 0) == 1593644
    assert C_layer(14, 1) == 531230
    assert C_layer(14, 2) == 177083


def test_unit_g_family():
    for t, K, a in ((1, 4, 1), (1, 5, -1), (2, 6, 4), (2, 5, 2)):
        for b in range(-4, 5):
            for c in range(-4, 5):
                assert unit_g_injective_mod(t, K, a, b, c)
                assert newton_stratum_q_unit_family(t, K, a, b, c)
                left = (g_poly(t, a, b) - g_poly(t, a, c)) % (3**K) == 0
                right = (b - c) % (3 ** (K - 1)) == 0
                assert left == right


def test_M_k_matches_image_through_k9():
    table = {2: 3, 3: 12, 4: 36, 5: 115, 6: 349, 7: 1074, 8: 3231, 9: 9780}
    for k, M in table.items():
        assert M_k_count(k) == M
        assert M_k_x3(k) == M
        assert same_depth_total(k) >= M
        assert same_depth_total(k) - M == states_report(k)["cross_depth_overlap"]


def test_zero_spine_is_not_the_whole_overlap():
    assert zero_spine_overcount(4) == 1
    assert zero_spine_overcount(6) == 2
    assert states_report(6)["cross_depth_overlap"] == 3
    assert states_report(6)["cross_depth_overlap"] > zero_spine_overcount(6)


@pytest.mark.slow
def test_M_k_arithmetic_table():
    table = {
        10: 29394,
        11: 88399,
        12: 265352,
        13: 796678,
        14: 2390443,
    }
    for k, M in table.items():
        assert M_k_count(k) == M
        assert raw_count_x3(k) == (3**k - 1) // 2


def test_layer_report_split():
    rec = layer_count_report(6, 1)
    assert rec["C"] == 80
    assert rec["raw"] == 81
    assert rec["injective"] == 54
    assert rec["q_image"] == 23
    assert rec["core_image"] == 26
    assert rec["overlap"] == 1
    shallow = layer_count_report(6, 3)
    assert shallow["C"] == 9
    assert shallow["injective"] == 9


def test_cli_x3_commands():
    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("x3-states", "--k", "5")
    assert "k = 5" in out
    assert "R_k = 121" in out
    assert "M_k = 115" in out
    assert "same-depth totals" in out
    assert "Q-image contributions" in out
    assert "cross-depth overlap" in out
    layer = _run("x3-layer-count", "--k", "6", "--deficit", "1")
    assert "C(k,k-1-r) = 80" in layer
    assert "raw layer size = 81" in layer
    assert "injective contribution = 54" in layer
    assert "Q-image contribution" in layer
    assert "overlap corrections = 1" in layer
    still = _run("newton-class", "x^3", "--k", "2")
    assert "class_id" in still
    cubic = _run("cubic-layer", "--k", "5", "--depth-deficit", "1")
    assert "C(k,k-2)" in cubic
    assert "shallow states" in out
    assert "R_k - M_k" in out
    ov = _run("x3-overlaps", "--k", "6")
    assert "zero spine" in ov
    assert "nonzero overlap families" in ov
    assert "total overcount = 3" in ov
    img = _run("x3-image-count", "--k", "6", "--deficit", "1")
    assert "N1/Q joint image = 26" in img
    assert "easy contribution = 54" in img
    assert "C(k,m) = 80" in img


def test_reduced_square_is_width():
    for k, r in ((6, 1), (8, 0), (9, 2), (10, 1)):
        assert square_modulus_exp(k, r) == k - 1 - 2 * r


def test_unit_square_is_plus_minus():
    k, r = 8, 1
    units = [u for u in core_u_range(k, r) if u % 3 != 0]
    for u in units:
        for v in units:
            if A_coord(u, k, r) == A_coord(v, k, r):
                assert u == v or u == -v


def test_joint_image_is_not_q_image():
    rec = image_count_report(6, 1)
    assert rec["joint_image"] == 26
    assert rec["q_image"] == 23
    assert rec["joint_image"] != rec["q_image"]
    assert rec["C"] == easy_count(4, 1) + rec["joint_image"]
    assert joint_image_size(6, 1) == rec["core_image"]


def test_overlaps_zero_spine_not_all():
    rec = overlaps_report(6)
    assert rec["zero_spine_overcount"] == 2
    assert rec["total_overcount"] == 3
    assert rec["nonzero_families"]
    assert "shared-sign" in rec["nonzero_families"] or "shared-sign" in rec["pair_counts"]


def test_n1_square_and_n0_neg_faces():
    k, r = 8, 1
    for u in (-5, -1, 1, 4, 9):
        for v in (-4, 1, 4, 9):
            assert newton_stratum_n1_square(k, r, u, v)
        assert newton_stratum_n0_neg(k, 6, u)
    W = square_modulus_exp(k, r)
    assert newton_stratum_unit_square(W, 4, -4)
    assert not newton_stratum_unit_square(W, 4, 5)
