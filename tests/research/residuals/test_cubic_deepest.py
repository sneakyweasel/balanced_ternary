"""Deepest-layer fibres of the residual machine of x^3."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from balanced_ternary.cli import main
from bt.calculus.cubic import F_k
from research.residuals.cubic_deepest import (
    C_km_neighbors,
    balanced_residue,
    cube_root_bound,
    cubic_quotient_congruence,
    deepest_F_k,
    deepest_class_count,
    deepest_equiv,
    deepest_fibre_of,
    deepest_image,
    deepest_n0,
    deepest_n0_decomp,
    deepest_n1,
    deepest_phi,
    fibre_kind,
    high_s0,
    high_stratum_count,
    large_unit_sign_prefixes,
    small_unit_sign_count,
    square_congruence,
    unit_sign_surplus,
    unit_stratum_count,
    zero_fibre,
    zero_fibre_size,
)
from research.residuals.cubic_fibres import C_km, balanced_bound, prefixes_at, zero_fibre_exponent
from bt.calculus.quadratic import iter_dz


def test_deepest_newton_simplification():
    for k in range(2, 9):
        mod = 3**k
        for p in prefixes_at(k - 1):
            N0, N1, N2, N3 = F_k(k - 1, p, k)
            assert N3 % mod == 0
            assert N2 % mod == 0
            assert N1 % mod == (3 * p * p) % mod
            assert N0 % mod == iter_dz(p**3, k - 1) % mod
            assert deepest_n1(p, k) == N1 % mod
            assert deepest_n0(p, k) == N0 % mod


def test_n0_is_balanced_quotient():
    for k in range(2, 8):
        for p in prefixes_at(k - 1):
            assert deepest_n0_decomp(p, k) == iter_dz(p**3, k - 1)
            bal = balanced_residue(p**3, k - 1)
            assert abs(bal) <= balanced_bound(k - 1)
            assert p**3 == bal + 3 ** (k - 1) * iter_dz(p**3, k - 1)


def test_fibre_criterion_matches_F_k():
    for k in range(2, 7):
        ps = list(prefixes_at(k - 1))
        for i, p in enumerate(ps):
            for q in ps[i:]:
                assert deepest_equiv(p, q, k) == (F_k(k - 1, p, k) == F_k(k - 1, q, k))
                assert square_congruence(p, q, k) == (deepest_n1(p, k) == deepest_n1(q, k))
                assert cubic_quotient_congruence(p, q, k) == (deepest_n0(p, k) == deepest_n0(q, k))


def test_units_collide_only_as_sign_pairs():
    for k in range(2, 8):
        image = deepest_image(k)
        for ps in image.values():
            units = [p for p in ps if p % 3 != 0]
            if len(units) <= 1:
                continue
            assert sorted(units) == [-units[-1], units[-1]] or (
                len(units) == 2 and units[0] == -units[1]
            )
            assert all(q in (-units[0], units[0]) for q in units)


def test_square_split_on_interval():
    # On P_{k-1}, 3^{k-1} | (p-q) forces p=q; 3^{k-1} | (p+q) forces p=-q.
    for k in range(2, 7):
        m = k - 1
        mod = 3**m
        for p in prefixes_at(m):
            for q in prefixes_at(m):
                if (p - q) % mod == 0:
                    assert p == q
                if (p + q) % mod == 0:
                    assert p == -q


def test_zero_fibre_theorem():
    for k in range(2, 13):
        r = zero_fibre_exponent(k)
        members = zero_fibre(k)
        expected = [p for p in prefixes_at(k - 1) if p % (3**r) == 0]
        assert members == expected
        assert len(members) == zero_fibre_size(k)
        zero = deepest_phi(0, k)
        assert all(deepest_phi(p, k) == zero for p in members)
        outsiders = [p for p in prefixes_at(k - 1) if p % (3**r) != 0]
        assert all(deepest_phi(p, k) != zero for p in outsiders)


def test_known_deepest_counts():
    table = {
        2: 2,
        3: 8,
        4: 24,
        5: 76,
        6: 232,
        7: 716,
        8: 2153,
        9: 6521,
        10: 19597,
        11: 58939,
        12: 176908,
        13: 531141,
        14: 1593644,
    }
    for k, C in table.items():
        assert deepest_class_count(k) == C
        assert C_km(k, k - 1) == C


def test_unit_stratum_and_small_signs():
    assert cube_root_bound(8) == 10
    assert small_unit_sign_count(8) == 7
    assert large_unit_sign_prefixes(8) == [907, 1093]
    assert unit_sign_surplus(8) == 9
    assert unit_stratum_count(8) == 2 * 3**6 - 9
    for k in range(3, 13):
        if k % 2 == 1:
            assert large_unit_sign_prefixes(k) == []
        else:
            B = balanced_bound(k - 1)
            larges = large_unit_sign_prefixes(k)
            assert B in larges


def test_high_stratum_closed_count():
    # k=8, s=4: unit cubes mod 27, six classes.
    assert high_s0(8) == 4
    assert high_stratum_count(8, 4) == 6
    assert high_stratum_count(7, 3) == 18
    assert high_stratum_count(7, 4) == 2
    assert high_stratum_count(10, 5) == 18
    image = deepest_image(8)
    size3 = [ps for ps in image.values() if len(ps) == 3]
    assert len(size3) == 6


def test_coset_conjecture_refuted_at_k8():
    image = deepest_image(8)
    twins = [sorted(ps) for ps in image.values() if fibre_kind(sorted(ps), 7) == "twin"]
    assert [720, 738] in twins
    assert [-738, -720] in twins


def test_deepest_fibre_of_sign_pair():
    assert deepest_fibre_of(1, 4) == [-1, 1]
    assert deepest_F_k(1, 4) == deepest_F_k(-1, 4)


def test_neighbors_diagnostic():
    rec = C_km_neighbors(6)
    assert rec["C_k_k-1"] == 232
    assert rec["C_k_k-2"] == C_km(6, 4)
    assert rec["C_k_k-3"] == C_km(6, 3)


def test_cli_cubic_deepest():
    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("cubic-deepest", "--k", "5")
    assert "C(k,k-1) = 76" in out
    assert "zero_fibre_size = 3" in out
    one = _run("cubic-deepest-fibre", "0", "--k", "5")
    assert "fibre_size = 3" in one
    assert "27" in one
