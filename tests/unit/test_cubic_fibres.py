"""Fibres of the cubic Newton image map."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from balanced_ternary.cli import main
from bt.calculus.cubic import F_k, M_k_x3, raw_count_x3
from bt.calculus.cubic_fibres import (
    C_km,
    balanced_bound,
    cross_depth_n3,
    fibre_of,
    fibre_report,
    n3_vanishes,
    per_depth_counts,
    prefixes_at,
    same_depth_equiv,
    same_depth_n0,
    same_depth_n1,
    same_depth_n2,
    sign_pair_equiv,
    zero_fibre_exponent,
    zero_spine_depths,
)
from bt.calculus.quadratic import iter_dz


def test_p_m_is_the_symmetric_interval():
    assert list(prefixes_at(0)) == [0]
    assert list(prefixes_at(1)) == [-1, 0, 1]
    assert list(prefixes_at(2)) == list(range(-4, 5))
    assert len(list(prefixes_at(5))) == 3**5
    assert balanced_bound(4) == 40


def test_same_depth_predicates_match_F_k():
    for k in range(2, 7):
        for m in range(k):
            ps = list(prefixes_at(m))
            for i, p in enumerate(ps):
                for q in ps[i:]:
                    assert same_depth_equiv(m, p, q, k) == (F_k(m, p, k) == F_k(m, q, k))


def test_n2_does_not_imply_n1():
    # Depth 1 at k=2: N2 is automatic, N1 separates 0 from ±1.
    assert same_depth_n2(1, 0, 1, 2)
    assert not same_depth_n1(1, 0, 1, 2)


def test_n21_does_not_imply_n0():
    # k=3, m=2, p=4, q=-4: N2 and N1 hold (sign, s=0) but |64| > 9 so N0 may fail.
    assert same_depth_n2(2, 4, -4, 3)
    assert same_depth_n1(2, 4, -4, 3)
    assert not same_depth_n0(2, 4, -4, 3)
    assert F_k(2, 4, 3) != F_k(2, -4, 3)


def test_sign_pair_criterion():
    assert sign_pair_equiv(1, 1, 2)
    assert not sign_pair_equiv(1, 1, 3)
    assert sign_pair_equiv(4, 3, 5)
    assert sign_pair_equiv(4, 3, 6)
    assert not sign_pair_equiv(4, 3, 7)
    assert sign_pair_equiv(4, 1, 5)
    assert not sign_pair_equiv(4, 1, 6)


def test_shallow_depth_is_uncompressed():
    for k in range(1, 9):
        for m in range(k):
            if 2 * m + 1 <= k:
                assert C_km(k, m) == 3**m


def test_per_depth_and_M_k():
    table = {
        2: ([1, 2], 3),
        3: ([1, 3, 8], 12),
        4: ([1, 3, 9, 24], 36),
        5: ([1, 3, 9, 27, 76], 115),
        6: ([1, 3, 9, 27, 80, 232], 349),
        7: ([1, 3, 9, 27, 81, 240, 716], 1074),
        8: ([1, 3, 9, 27, 81, 243, 721, 2153], 3231),
        9: ([1, 3, 9, 27, 81, 243, 727, 2178, 6521], 9780),
    }
    for k, (Cs, M) in table.items():
        assert per_depth_counts(k) == Cs
        assert M_k_x3(k) == M
        assert sum(Cs) >= M
        xs = fibre_report(k)["cross_depth"]
        if k < 4:
            assert xs == []
        assert M == len({F_k(m, p, k) for m in range(k) for p in prefixes_at(m)})


def test_zero_fibre_at_deepest_layer():
    for k in range(4, 13):
        r = zero_fibre_exponent(k)
        m = k - 1
        zero = F_k(m, 0, k)
        members = [p for p in prefixes_at(m) if F_k(m, p, k) == zero]
        expected = [p for p in prefixes_at(m) if p % (3**r) == 0]
        assert members == expected
        assert len(members) == 3 ** (m - r)


def test_n3_cross_depth_gate():
    for k in range(1, 9):
        for m in range(k):
            for n in range(k):
                if m == n:
                    continue
                can = cross_depth_n3(m, n, k)
                if not can:
                    # Distinct N3 residues forbid any collision.
                    assert n3_vanishes(m, k) is False or n3_vanishes(n, k) is False
                    assert F_k(m, 0, k) != F_k(n, 0, k) or not (
                        n3_vanishes(m, k) and n3_vanishes(n, k)
                    )


def test_zero_spine():
    assert zero_spine_depths(4) == [2, 3]
    assert zero_spine_depths(5) == [3, 4]
    assert zero_spine_depths(6) == [3, 4, 5]
    assert zero_spine_depths(8) == [4, 5, 6, 7]
    for k in (4, 5, 6, 7, 8):
        depths = zero_spine_depths(k)
        phis = {F_k(m, 0, k) for m in depths}
        assert len(phis) == 1


def test_fibre_of_first_merge():
    fib = fibre_of(1, 1, 2)
    assert sorted(fib) == [(1, -1), (1, 1)]


def test_cli_cubic_fibres():
    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("cubic-fibres", "--k", "4")
    assert "M_k = 36" in out
    assert "per_depth" in out
    one = _run("cubic-fibre", "1", "1", "--k", "2")
    assert "fibre_size = 2" in one
    assert "(1, -1)" in one


def test_extended_image_table():
    # Arithmetic image only; not the automata minimizer.
    extra = {10: 29394, 11: 88399, 12: 265352}
    for k, M in extra.items():
        assert M_k_x3(k) == M
        assert M <= raw_count_x3(k)
        assert iter_dz(0, k) == 0
