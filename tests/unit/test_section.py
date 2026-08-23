"""Section derivative on ordinary Z[x]."""

from __future__ import annotations

from bt.calculus.section import (
    IntPoly,
    classical_chain,
    classical_leibniz,
    composition_law,
    degree_drops,
    parse_poly,
    section_reconstruction,
    twisted_leibniz,
)


FS = (
    parse_poly("x"),
    parse_poly("2x+1"),
    parse_poly("x^2"),
    parse_poly("x^2+x"),
    parse_poly("x^3"),
)
GS = (
    parse_poly("3x+1"),
    parse_poly("x+1"),
    parse_poly("2x-1"),
    parse_poly("x^2"),
)


def test_parse_and_eval():
    f = parse_poly("x^2+x")
    assert f.eval(3) == 12
    assert parse_poly("2x+1").eval(-1) == -1
    assert parse_poly("-3").coeffs == (-3,)


def test_closure_and_reconstruction():
    for f in FS + GS + (parse_poly("x^4"),):
        for a in (-1, 0, 1, 2, -4):
            df = f.section_deriv(a)
            assert all(isinstance(c, int) for c in df.coeffs)
            for x in range(-8, 9):
                assert section_reconstruction(f, a, x)


def test_twisted_leibniz_and_not_classical():
    hits = 0
    for f in FS:
        for g in GS:
            for a in (-1, 0, 1):
                assert twisted_leibniz(f, g, a)
                if not classical_leibniz(f, g, a):
                    hits += 1
    assert hits > 0


def test_composition_law_and_not_classical_chain():
    fails_classical = 0
    for f in FS:
        for g in GS:
            for a in (-1, 0, 1):
                assert composition_law(f, g, a)
                if not classical_chain(f, g, a):
                    fails_classical += 1
    assert fails_classical > 0


def test_degree_not_lowered():
    f = parse_poly("x^2")
    assert f.degree == 2
    for a in (-1, 0, 1):
        df = f.section_deriv(a)
        assert df.degree == 2
        assert df.lc() == 3 ** (f.degree - 1) * f.lc()
        assert not degree_drops(f, a)


def test_lc_recurrence():
    for d, f in (
        (1, parse_poly("2x+1")),
        (2, parse_poly("x^2")),
        (3, parse_poly("x^3")),
        (4, parse_poly("x^4")),
    ):
        for a in (-1, 0, 1):
            df = f.section_deriv(a)
            assert df.degree == d
            assert df.lc() == 3 ** (d - 1) * f.lc()
            d2 = df.section_deriv(a)
            assert d2.lc() == 3 ** (d - 1) * df.lc()
