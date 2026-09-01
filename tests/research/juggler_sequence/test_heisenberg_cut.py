"""Heisenberg cut regularity: no atom, fiber agrees, anti-overclaim."""

from __future__ import annotations

import numpy as np

from research.juggler_sequence.heisenberg_cut import (
    ANTI,
    CLASS_GREEN,
    TEST_WINDOW,
    build_summary,
    cut_conditioned,
    cut_mass,
)


def test_uniform_synthetic_has_no_atom():
    rng = np.random.default_rng(0)
    frac = rng.random(20_000)
    mass = cut_mass(frac)
    assert mass["no_atom"]
    assert mass["exact_zeros_order_p_quarter"]


def test_atom_is_detected():
    frac = np.zeros(5_000)
    frac[:100] = 0.0
    frac[100:] = np.linspace(0.1, 0.9, 4_900)
    mass = cut_mass(frac)
    assert not mass["no_atom"]


def test_conditioned_agrees_when_independent():
    rng = np.random.default_rng(1)
    frac = rng.random(20_000)
    vertical = rng.random(20_000)
    cond = cut_conditioned(frac, vertical)
    assert cond["fiber_agrees"]


def test_exact_zero_is_perfect_square_m():
    from math import isqrt

    from research.juggler_sequence.bracket_nil_lift import tower_data

    hits = []
    for n in range(1001, 20000, 2):
        d = tower_data(n)
        if d["frac_B"] == 0.0:
            v = d["v"]
            k = isqrt(v)
            assert k * k == v
            hits.append(n)
    assert hits  # at least one square landing in the range


def test_summary_green_and_anti_overclaim():
    summary = build_summary(n_max=TEST_WINDOW)
    assert summary["decision"]["classification"] == CLASS_GREEN
    assert not ANTI["equidistribution_claimed"]
    assert not ANTI["characteristic_factor_claimed"]
    assert not ANTI["k3_bound_claimed"]
    assert not ANTI["toolkit_reopened"]
    assert not ANTI["paper_b_modified"]
