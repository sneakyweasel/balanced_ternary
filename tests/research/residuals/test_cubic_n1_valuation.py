"""General N1 refinement after the N2 depth-deficit filter."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from balanced_ternary.cli import main
from research.residuals.cubic_fibres import prefixes_at, same_depth_n1, same_depth_n2
from research.residuals.cubic_n1_valuation import (
    deficit_depth,
    low_val_collisions,
    n1_after_n2,
    n1_high_val_reduces,
    n1_strata_report,
    n21_agree,
    n21_class_count,
    n21_fibre_of,
    n21_image,
    n2_image,
    surviving_locus_ok,
)
from bt.metrics import v3


def test_n1_after_n2_factorization():
    for r in range(0, 5):
        for k in range(r + 1, r + 6):
            m = k - 1 - r
            for p in prefixes_at(m):
                for q in prefixes_at(m):
                    if (p - q) % (3**r) != 0:
                        continue
                    delta = (p - q) // (3**r)
                    rhs = (delta * (p + q + 3**m)) % (3 ** (k - 1 - r)) == 0
                    assert n1_after_n2(p, q, k, r) is rhs
                    assert n1_after_n2(p, q, k, r) is same_depth_n1(m, p, q, k)


def test_n2_class_count_is_three_pow_r():
    for r in range(0, 5):
        for k in range(max(r + 1, 2 * r + 1), 2 * r + 5):
            assert len(n2_image(k, r)) == 3**r


def test_unit_injectivity_r_ge_1():
    for r in range(1, 5):
        for k in range(r + 1, r + 6):
            m = k - 1 - r
            for p in prefixes_at(m):
                if p % 3 == 0:
                    continue
                assert n21_fibre_of(p, k, r) == [p]


def test_r0_units_can_collide():
    # At deficit 0, N2 is vacuous and sign pairs survive N1.
    assert n21_agree(1, -1, 4, 0)
    fib = n21_fibre_of(1, 4, 0)
    assert -1 in fib and 1 in fib


def test_low_val_separated():
    for r in range(1, 5):
        for k in range(r + 1, r + 6):
            assert low_val_collisions(k, r) == []
            assert surviving_locus_ok(k, r)


def test_surviving_fibres_in_3r():
    cases = [(1, 6), (1, 7), (2, 7), (2, 8), (3, 8), (3, 9), (4, 10), (5, 11)]
    for r, k in cases:
        assert surviving_locus_ok(k, r)
        step = 3**r
        for ps in n21_image(k, r).values():
            if len(ps) <= 1:
                continue
            assert all(p % step == 0 for p in ps)


def test_sign_pairs_iff_3r_divides():
    for r in range(0, 5):
        for k in range(r + 1, r + 6):
            m = k - 1 - r
            for p in prefixes_at(m):
                if abs(p) > (3**m - 1) // 2:
                    continue
                if abs(-p) > (3**m - 1) // 2:
                    continue
                expect = p % (3**r) == 0
                assert same_depth_n2(m, p, -p, k) is expect
                assert same_depth_n1(m, p, -p, k) is expect
                if expect and p != 0:
                    assert -p in n21_fibre_of(p, k, r)


def test_recovers_r1_and_r2():
    rec1 = n1_strata_report(6, 1)
    assert rec1["m"] == 4
    assert rec1["N2"] == 3
    assert rec1["unit_classes"] == rec1["unit_prefixes"]
    assert rec1["surviving_in_3r"]
    assert all(all(p % 3 == 0 for p in fib) for fib in rec1["examples"])

    rec2 = n1_strata_report(7, 2)
    assert rec2["m"] == 4
    assert rec2["N2"] == 9
    assert rec2["unit_classes"] == rec2["unit_prefixes"]
    assert rec2["surviving_in_3r"]
    assert all(all(p % 9 == 0 for p in fib) for fib in rec2["examples"])


def test_scaled_n1_reduction():
    for r in range(1, 4):
        k = 2 * r + 3
        m = k - 1 - r
        bound = (3**m - 1) // 2
        for u in range(-4, 5):
            for v in range(-4, 5):
                if abs(3**r * u) > bound or abs(3**r * v) > bound:
                    continue
                assert n1_high_val_reduces(k, r, u, v)


def test_k_eq_2r_plus_1_n1_automatic_on_locus():
    for r in range(1, 4):
        k = 2 * r + 1
        m = k - 1 - r
        step = 3**r
        locus = [p for p in prefixes_at(m) if p % step == 0]
        for i, p in enumerate(locus):
            for q in locus[i:]:
                assert n1_after_n2(p, q, k, r)


def test_no_low_val_obstruction_larger():
    # Push past r=2; still no counterexample to the valuation theorem.
    for r, k in [(3, 9), (4, 10), (5, 12)]:
        assert low_val_collisions(k, r) == []
        rec = n1_strata_report(k, r)
        assert rec["N2"] == 3**r
        assert rec["surviving_in_3r"]
        assert rec["unit_classes"] == rec["unit_prefixes"]


def test_report_and_cli():
    rec = n1_strata_report(7, 2)
    assert rec["k"] == 7
    assert rec["m"] == 4
    assert rec["r"] == 2
    assert rec["N2"] == 9
    assert rec["surviving_in_3r"]
    assert deficit_depth(7, 2) == 4
    assert n21_class_count(7, 2) == rec["N21"]

    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("n1-strata", "--k", "7", "--deficit", "2")
    assert "depth m = 4" in out
    assert "deficit r = 2" in out
    assert "N2 classes = 9" in out
    assert "surviving in 3^2 Z = True" in out
    one = _run("n1-fibre", "0", "--k", "9", "--deficit", "2")
    assert "fibre_size =" in one
    assert "depth m = 6" in one
    still = _run("cubic-layer", "--k", "6", "--depth-deficit", "1")
    assert "C(k,k-2) = 80" in still


def test_v3_none_is_zero():
    assert v3(0) is None
    assert v3(9) == 2
    assert v3(1) == 0
