"""PS-inversion barrier: exact seal, exponent chain, bias-mass relaxation."""

from __future__ import annotations

from math import isqrt, log
from pathlib import Path

from research.juggler_sequence.ps_inversion_barrier import (
    BOURGAIN_PAIR,
    DENSITY_EXPONENT,
    EPC_PAIR,
    MAIN_TERM_EXPONENT,
    SBITS,
    VDC_EXPONENT,
    ceil_cbrt,
    floor_m94_scaled,
    frac_half_m94,
    pair_functional,
    r_of_m,
    seal_identity,
    v_of_n,
)

DOSSIER = Path("docs/problems/juggler_ps_inversion_barrier.md")

GAMMA = log(2.0) / log(3.0)


def test_seal_identity_small():
    seal = seal_identity(1500)
    assert seal["abs_gap"] < 1e-9
    assert seal["r_sum_equals_N"]
    assert seal["r_outside_01"] == 0


def test_ps_indicator_is_zero_one_and_counts():
    n_max = 400
    m_max = v_of_n(n_max)
    total = 0
    for m in range(1, m_max + 1):
        r = r_of_m(m)
        assert r in (0, 1)
        total += r
    assert total == n_max
    # Direct membership cross-check on a window.
    image = {v_of_n(n) for n in range(1, n_max + 1)}
    for m in range(1, m_max + 1):
        assert (m in image) == (r_of_m(m) == 1)


def test_frac94_exact_on_fourth_powers():
    # m = k^4 gives m^{9/4} = k^9 exactly: fractional part 0.
    for k in (2, 3, 7, 20):
        m = k**4
        t = floor_m94_scaled(m)
        assert t == (k**9) << SBITS
        assert frac_half_m94(m) in (0.0, 0.5)


def test_frac94_scale_consistency():
    for m in (17, 12345, 999983, 40000000):
        t64 = floor_m94_scaled(m, 64)
        t96 = floor_m94_scaled(m, 96)
        f64 = (t64 % (1 << 64)) / float(1 << 64)
        f96 = (t96 % (1 << 96)) / float(1 << 96)
        assert abs(f64 - f96) < 2.0**-60


def test_ceil_cbrt_exact():
    for y in (1, 7, 8, 9, 26, 27, 28, 10**12, 10**12 + 1):
        n = ceil_cbrt(y)
        assert n**3 >= y > (n - 1) ** 3


def test_main_term_exponent_chain():
    # Main term saving sits below the density barrier; vdC sits above it.
    assert MAIN_TERM_EXPONENT == 13.0 / 24.0
    assert MAIN_TERM_EXPONENT < DENSITY_EXPONENT < VDC_EXPONENT
    # In n-units: M^{13/24} = N^{13/16} (M = N^{3/2}), a power saving.
    assert 1.5 * MAIN_TERM_EXPONENT == 13.0 / 16.0 < 1.0


def test_exponent_pair_functional_gap():
    # T_j block bound is M^{(5/4)p+q}; the door needs (5/4)p + q < 2/3.
    bourgain = pair_functional(BOURGAIN_PAIR)
    assert abs(bourgain - 95.0 / 112.0) < 1e-12
    assert bourgain > DENSITY_EXPONENT
    # Classical vdC pairs land exactly on 7/8.
    assert abs(pair_functional((1.0 / 6.0, 2.0 / 3.0)) - 7.0 / 8.0) < 1e-12
    assert abs(pair_functional((1.0 / 14.0, 11.0 / 14.0)) - 7.0 / 8.0) < 1e-12
    # The exponent-pair conjecture point would clear the barrier with room.
    assert pair_functional(EPC_PAIR) < DENSITY_EXPONENT


def _relative_entropy(p: float, q: float) -> float:
    return p * log(p / q) + (1.0 - p) * log((1.0 - p) / (1.0 - q))


def test_bias_mass_relaxation_chernoff_positive():
    """Lemma B with 'every node' weakened to 'all but vanishing mass'.

    Paths hitting >= delta*d biased nodes have mass o(1)/delta (Markov on
    the expected biased-node count).  On the rest, the O-count at unbiased
    nodes obeys the Lemma B domination, and never-contracting still needs
    o_d >= gamma*d, so the Chernoff rate is D((gamma-delta)/(1-delta) || 1-beta),
    positive as soon as delta < (gamma - (1-beta)) / beta.
    """
    beta, delta = 0.40, 0.05
    threshold = (GAMMA - delta) / (1.0 - delta)
    assert threshold > 1.0 - beta
    assert _relative_entropy(threshold, 1.0 - beta) > 0.0
    # delta -> 0 recovers Lemma B's condition gamma > 1 - beta.
    assert GAMMA > 1.0 - beta


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
    assert "95/112" in dossier
    assert "13/24" in dossier
    assert "No new ledger row" in dossier or "no new ledger row" in dossier.lower()
    assert "bourgain-2017-exponent-pair" in dossier
