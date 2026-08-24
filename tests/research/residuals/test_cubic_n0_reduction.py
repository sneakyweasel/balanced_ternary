"""N0 scaling on the 3^r-divisible locus."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from cli.main import main
from research.residuals.cubic_fibres import prefixes_at, same_depth_n0
from research.residuals.cubic_n0_reduction import (
    n0_candidate_deepest,
    n0_fibre_after_n21,
    n0_mod,
    n0_original,
    n0_reduction_report,
    n0_regime,
    n0_scaled,
    n0_visibility_bound,
    n0_visible_mod,
    phase_row,
    reduced_depth,
    u_prefixes,
)
from research.residuals.cubic_n1_valuation import deficit_depth, n21_agree
from bt.calculus.quadratic import iter_dz


def test_two_regime_formula():
    for r in range(0, 5):
        for k in range(r + 1, r + 10):
            for u in u_prefixes(k, r):
                assert n0_original(u, k, r) == n0_scaled(u, k, r)


def test_unexhausted_is_scaled_cube():
    r, k = 2, 8  # m=5, 3r=6, unexhausted
    assert n0_regime(k, r) == "unexhausted"
    m = deficit_depth(k, r)
    for u in u_prefixes(k, r):
        assert n0_scaled(u, k, r) == (3 ** (3 * r - m)) * (u**3)


def test_exhausted_is_iterated_cube():
    r, k = 1, 8  # m=6, 3r=3, exhausted t=3
    assert n0_regime(k, r) == "exhausted"
    t = reduced_depth(k, r)
    assert t == k - 1 - 4 * r
    for u in u_prefixes(k, r):
        assert n0_scaled(u, k, r) == iter_dz(u**3, t)


def test_boundary_agrees():
    r, k = 1, 5  # m=3=3r
    assert n0_regime(k, r) == "boundary"
    for u in u_prefixes(k, r):
        assert n0_scaled(u, k, r) == u**3
        assert n0_scaled(u, k, r) == iter_dz(u**3, 0)


def test_not_standard_deepest_at_n1_horizon():
    # r≥1, exhausted: N0 depth is not the deepest depth at horizon k-2r.
    r, k = 1, 8
    assert reduced_depth(k, r) != k - 2 * r - 1
    mismatches = 0
    mod = 3 ** (k - 2 * r)
    for u in u_prefixes(k, r):
        a = n0_mod(u, k, r) % mod
        b = n0_candidate_deepest(u, k, r) % mod
        if a != b:
            mismatches += 1
    assert mismatches > 0


def test_sign_survives_iff_n0_zero():
    for r in range(1, 4):
        for k in range(r + 1, r + 7):
            m = deficit_depth(k, r)
            for p in prefixes_at(m):
                if p % (3**r) != 0:
                    continue
                if abs(-p) > (3**m - 1) // 2:
                    continue
                survives = same_depth_n0(m, p, -p, k)
                assert survives == (iter_dz(p**3, m) % (3**k) == 0)


def test_visibility_bound():
    for t, k in [(0, 2), (1, 3), (2, 4), (3, 5)]:
        s = n0_visibility_bound(t, k)
        assert s == max(1, t + k - 1)
        for u in range(-12, 13):
            for w in range(-2, 3):
                v = u + w * (3**s)
                assert n0_visible_mod(t, k, s, u, v)


def test_visibility_bound_is_sharp():
    t, k = 1, 2
    s = n0_visibility_bound(t, k)  # 2
    assert not n0_visible_mod(t, k, s - 1, 1, 1 + 3 ** (s - 1))


def test_phase_threshold_is_m_minus_3s():
    row = phase_row(8, 1, 1)
    assert row["m_minus_3s"] == 6 - 3
    assert row["regime"] == "exhausted"
    row2 = phase_row(8, 2, 2)
    assert row2["m"] == 5
    assert row2["regime"] == "unexhausted"


def test_report_and_cli():
    rec = n0_reduction_report(8, 1)
    assert rec["regime"] == "exhausted"
    assert rec["t"] == 3
    assert rec["formula_ok"]
    assert rec["depth_mismatch"]

    rec2 = n0_reduction_report(8, 2)
    assert rec2["unexhausted"]
    assert rec2["formula_ok"]

    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("n0-reduction", "--k", "8", "--deficit", "1")
    assert "depth m = 6" in out
    assert "regime = exhausted" in out
    assert "reduced depth t = 3" in out
    assert "formula ok = True" in out
    one = _run("n0-fibre", "0", "--k", "9", "--deficit", "2")
    assert "N0 fibre_size =" in one
    still = _run("n1-strata", "--k", "7", "--deficit", "2")
    assert "N2 classes = 9" in still


def test_n0_fibre_is_n21_refined():
    members = n0_fibre_after_n21(0, 9, 2)
    n21_ok = all(n21_agree(0, q, 9, 2) for q in members)
    assert n21_ok
    assert 0 in members
    # Milestone 23: full Newton fibre of 0 at k=9, r=2 is {-243,0,243}.
    assert members == [-243, 0, 243]
