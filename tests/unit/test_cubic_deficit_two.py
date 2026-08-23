"""Depth-deficit 2 cubic layer: m = k-3."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from balanced_ternary.cli import main
from bt.calculus.cubic import F_k
from bt.calculus.cubic_deficit_two import (
    def2_class_count,
    def2_equiv,
    def2_fibre_of,
    def2_n1,
    def2_n2,
    def2_n2_agree,
    def2_report,
    deficit_two_depth,
    horizon_surplus,
    n21_image,
    n2_image,
)
from bt.calculus.cubic_fibres import C_km, prefixes_at, same_depth_n2
from bt.calculus.quadratic import iter_dz


def test_newton_simplification():
    for k in range(5, 9):
        mod = 3**k
        m = k - 3
        for p in prefixes_at(m):
            N0, N1, N2, N3 = F_k(m, p, k)
            assert N3 % mod == 0
            assert N2 % mod == (2 * 3 ** (k - 2) * p) % mod
            assert def2_n2(p, k) == N2 % mod
            assert N0 % mod == iter_dz(p**3, m) % mod
            if k >= 6:
                assert N1 % mod == (3 * p * p + 3 ** (k - 2) * p) % mod
                assert def2_n1(p, k) == N1 % mod


def test_n2_visibility_mod9():
    for k in range(3, 9):
        ps = list(prefixes_at(k - 3))
        for i, p in enumerate(ps):
            for q in ps[i:]:
                assert def2_n2_agree(p, q, k) == ((p - q) % 9 == 0)
                assert def2_equiv(p, q, k) == (F_k(k - 3, p, k) == F_k(k - 3, q, k))


def test_general_visibility_small():
    for r in range(0, 4):
        for k in range(r + 1, r + 5):
            m = k - 1 - r
            ps = list(prefixes_at(m))
            for i, p in enumerate(ps):
                for q in ps[i:]:
                    assert same_depth_n2(m, p, q, k) == ((p - q) % (3**r) == 0)


def test_n2_has_nine_classes():
    assert len(n2_image(3)) == 1
    assert len(n2_image(4)) == 3
    for k in range(5, 12):
        assert len(n2_image(k)) == 9


def test_n21_strictly_below_full():
    for k in range(6, 11):
        n21 = len(n21_image(k))
        full = def2_class_count(k)
        assert n21 < full


def test_known_counts():
    table = {
        3: 1,
        4: 3,
        5: 9,
        6: 27,
        7: 81,
        8: 243,
        9: 727,
        10: 2180,
        11: 6554,
        12: 19661,
    }
    for k, C in table.items():
        assert def2_class_count(k) == C
        assert C_km(k, k - 3) == C


def test_uncompressed_through_k8():
    for k in range(3, 9):
        assert def2_class_count(k) == 3 ** (k - 3)


def test_surplus_table():
    deltas = {7: 1, 8: 3, 9: 6, 10: 2, 11: 17, 12: 9}
    for k, d in deltas.items():
        assert horizon_surplus(k) == d
        assert def2_class_count(k) - C_km(k - 1, k - 3) == d


def test_unit_residues_are_singletons():
    for k in range(6, 10):
        for p in prefixes_at(k - 3):
            if p % 3 == 0:
                continue
            assert def2_fibre_of(p, k) == [p]


def test_sign_n2_requires_nine():
    for k in range(5, 10):
        for p in prefixes_at(k - 3):
            assert def2_n2_agree(p, -p, k) == (p % 9 == 0)


def test_first_collision_is_zero_coset():
    assert def2_fibre_of(0, 9) == [-243, 0, 243]
    assert def2_class_count(9) == 727


def test_report_and_cli():
    rec = def2_report(7)
    assert rec["k"] == 7
    assert rec["m"] == 4
    assert rec["N2"] == 9
    assert rec["C"] == 81
    assert rec["Delta"] == 1

    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("cubic-layer", "--k", "7", "--depth-deficit", "2")
    assert "m = 4" in out
    assert "N2 classes = 9" in out
    assert "C(k,k-3) = 81" in out
    one = _run("cubic-layer-fibre", "0", "--k", "9", "--depth-deficit", "2")
    assert "fibre_size = 3" in one
    still = _run("cubic-layer", "--k", "6", "--depth-deficit", "1")
    assert "C(k,k-2) = 80" in still


def test_depth_rejects_other_deficits():
    assert deficit_two_depth(8) == 5
    try:
        from bt.calculus.cubic_layer import layer_depth

        layer_depth(8, 2)
    except ValueError:
        return
    raise AssertionError("r=1 module must still reject deficit 2")
