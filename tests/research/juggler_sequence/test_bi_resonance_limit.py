"""BI resonance ceiling: the sub-density barrier is beyond the method's dream.

All arithmetic exact (fractions). The question answered NO:
sub-density on T_j needs an exponent pair with (5/4)p + q < 2/3,
i.e. p < 2/27 on the BI line q = p + 1/2, while the Bombieri-Iwaniec
method's structural ceiling (both spacing problems resolved perfectly)
is the zeta-exponent floor p = 3/20 -- a factor 81/40 = 2.025 short.
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path

DOSSIER = Path("docs/problems/juggler_bi_resonance_limit.md")

HALF = F(1, 2)
DENSITY = F(2, 3)  # the sub-density target for the functional (5/4)p + q
NEEDED_P = F(2, 27)  # threshold on the BI line
BI_CEILING = F(3, 20)  # both spacing problems perfect (Huxley / EoM)
BOURGAIN = F(13, 84)  # decoupling: first spacing problem optimal
HUXLEY_2005 = F(32, 205)
HUXLEY_1993 = F(89, 570)
BOMBIERI_IWANIEC_1986 = F(9, 56)


def phi(p: F, q: F) -> F:
    """The T_j block functional: exponent pair (p, q) gives M^{(5/4)p+q}."""
    return F(5, 4) * p + q


def transform_a(p: F, q: F) -> tuple[F, F]:
    d = 2 * p + 2
    return p / d, (p + q + 1) / d


def transform_b(p: F, q: F) -> tuple[F, F]:
    return q - HALF, p + HALF


def test_half_line_criterion_is_exact():
    # On q = p + 1/2 the functional is (9/4)p + 1/2; equality with 2/3
    # at exactly p = 2/27.
    for p in (F(0), F(1, 100), NEEDED_P, BI_CEILING, BOURGAIN):
        assert phi(p, p + HALF) == F(9, 4) * p + HALF
    assert phi(NEEDED_P, NEEDED_P + HALF) == DENSITY
    assert phi(NEEDED_P - F(1, 1000), NEEDED_P - F(1, 1000) + HALF) < DENSITY


def test_zeta_exponent_equals_p_on_half_line():
    # Zeta normalization: theta = (p+q)/2 - 1/4 = p when q = p + 1/2,
    # so the method's zeta floor 3/20 is a floor for p.
    for p in (BI_CEILING, BOURGAIN, HUXLEY_2005, HUXLEY_1993):
        q = p + HALF
        assert (p + q) / 2 - F(1, 4) == p


def test_historical_pairs_sit_on_half_line():
    assert HUXLEY_2005 + HALF == F(269, 410)
    assert BOURGAIN + HALF == F(55, 84)


def test_ceiling_chain_and_margin():
    # needed < dream ceiling < everything achieved.
    chain = (
        NEEDED_P,
        BI_CEILING,
        BOURGAIN,
        HUXLEY_2005,
        HUXLEY_1993,
        BOMBIERI_IWANIEC_1986,
    )
    assert all(a < b for a, b in zip(chain, chain[1:]))
    # The exact margin: even the dream misses by 81/40.
    assert BI_CEILING / NEEDED_P == F(81, 40)
    # Dream-ceiling functional still far above density.
    assert phi(BI_CEILING, BI_CEILING + HALF) == F(67, 80) > DENSITY
    # Today's frontier functional (recorded last phase).
    assert phi(BOURGAIN, BOURGAIN + HALF) == F(95, 112) > DENSITY


def test_b_fixes_and_a_worsens_below_one_sixth():
    # B fixes the half-line; A worsens the functional iff p < 1/6
    # (exact root: 9p^2 + (9/2)p - 1 = 0 at p = 1/6), and every
    # historical BI pair has p < 1/6.
    p_root = F(1, 6)
    assert 9 * p_root**2 + F(9, 2) * p_root - 1 == 0
    for p in (BI_CEILING, BOURGAIN, HUXLEY_2005, HUXLEY_1993, BOMBIERI_IWANIEC_1986):
        q = p + HALF
        assert p < p_root
        assert transform_b(p, q) == (p, q)
        assert phi(*transform_a(p, q)) > phi(p, q)


def test_regime_is_middle_range():
    # alpha = log M / log T = 1/(9/4) = 4/9 sits between Sargos's 2/5
    # variant and the classical BI 1/2: no boundary loophole.
    alpha = F(4, 9)
    assert F(2, 5) < alpha < F(1, 2)


def test_dossier_headings_and_close():
    dossier = DOSSIER.read_text(encoding="utf-8")
    for heading in (
        "## Problem",
        "## Exact statement",
        "## Current literature",
        "## Branch budget",
        "## Decision",
        "## Publication assessment",
    ):
        assert heading in dossier
    decision = dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "CLOSE" in decision
    assert "3/20" in dossier
    assert "2/27" in dossier
    assert "81/40" in dossier
    assert "huxley-1996-area-lattice-points" in dossier
    assert "huxley-2005-zeta-v" in dossier
    assert "No new ledger row" in dossier or "no new ledger row" in dossier.lower()
