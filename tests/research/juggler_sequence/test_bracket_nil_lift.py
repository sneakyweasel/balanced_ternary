"""Heisenberg lift probe: exact roots, bracket identity, censuses."""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from math import floor, isqrt

from research.juggler_sequence.bracket_nil_lift import (
    ANTI,
    CLASS_GREEN,
    TAYLOR_CONSTANT,
    TEST_WINDOW,
    build_summary,
    expansion_check,
    scaled_root4,
    scaled_sqrt,
    tower_data,
)


def test_scaled_roots_match_decimal():
    getcontext().prec = 60
    for m in (2, 10**6 + 7, 3**40, 123456789012345):
        d = 20
        r2 = scaled_sqrt(m, d)
        want2 = int(Decimal(m).sqrt() * 10**d)
        assert abs(r2 - want2) <= 1
        r4 = scaled_root4(m, d)
        want4 = int(Decimal(m).sqrt().sqrt() * 10**d)
        assert abs(r4 - want4) <= 1


def test_bracket_identity_exact():
    # A {B} = A B - A floor(B) for exact rationals
    for a_num, b_num in ((37, 155), (12345, 998), (7, 3)):
        A = Fraction(a_num, 13)
        B = Fraction(b_num, 17)
        lhs = A * (B - floor(B))
        rhs = A * B - A * floor(B)
        assert lhs == rhs


def test_tower_data_consistency():
    for n in (10001, 54321, 99999):
        d = tower_data(n)
        v = isqrt(n**3)
        assert d["v"] == v
        assert d["z"] == isqrt(v**3)
        assert 0.0 <= d["theta"] < 1.0
        for key in ("frac_A", "frac_B", "frac_C", "vertical", "abelian"):
            assert 0.0 <= d[key] < 1.0
        # {A floor(B)} + {A {B}} == {A B} mod 1 (integer mod before floats)
        den = 2 * 10**44
        a_theta = ((3 * d["r_a34"] * (d["r_b"] % 10**22)) % den) / den
        ab = ((3 * d["r_a34"] * d["r_b"]) % den) / den
        diff = abs((d["vertical"] + a_theta) % 1.0 - ab)
        assert min(diff, 1.0 - diff) < 1e-9


def test_expansion_bound_holds_on_window():
    result = expansion_check(TEST_WINDOW)
    assert result["bound_holds"]
    assert result["worst_taylor_ratio"] <= TAYLOR_CONSTANT * (1.0 + 1e-6)
    assert result["max_abs_r"] < 1e-5


def test_summary_green_and_anti_overclaim():
    summary = build_summary(n_max=TEST_WINDOW)
    assert summary["decision"]["classification"] == CLASS_GREEN
    assert not ANTI["equidistribution_claimed"]
    assert not ANTI["k3_bound_claimed"]
    assert not ANTI["toolkit_reopened"]
    assert not ANTI["paper_b_modified"]
