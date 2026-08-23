"""D-locality of binary maps; lattice ops commute with D."""

from __future__ import annotations

from research.rewrite_calculus.jet_local_ops import (
    WINDOW,
    affine_dH_d_local,
    named_report,
)
from bt.calculus.derivative import D


def test_max_min_commute_with_D():
    for x in WINDOW:
        for y in WINDOW:
            assert D(max(x, y)) == max(D(x), D(y))
            assert D(min(x, y)) == min(D(x), D(y))


def test_named_locality():
    rows = {row["name"]: row for row in named_report()}
    assert rows["add"]["H_d_local"] is False
    assert rows["add"]["DH_d_local"] is False
    assert rows["mul"]["DH_d_local"] is False
    assert rows["gcd"]["DH_d_local"] is False
    assert rows["max"]["DH_d_local"] is True
    assert rows["min"]["DH_d_local"] is True
    assert rows["D_max"]["H_d_local"] is True
    assert rows["D_min"]["H_d_local"] is True
    assert rows["max"]["H_d_local"] is False


def test_affine_DH_d_local_is_unary_slope_one_or_constant():
    hits = set(affine_dH_d_local())
    assert (0, 0, 0, 0) in hits
    assert (0, 1, 0, 0) in hits
    assert (0, 0, 1, 0) in hits
    assert (1, 0, 0, 0) not in hits
    assert (0, 1, 1, 0) not in hits
    for a, b, c, d in hits:
        assert a == 0
        assert (b, c) in {(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)}
