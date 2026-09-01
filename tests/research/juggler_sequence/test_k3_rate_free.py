"""Rate-free reduction probe: exact profiles, tower bins, wiring."""

from __future__ import annotations

from decimal import Decimal, getcontext

from research.juggler_sequence.k3_rate_free import (
    ANTI,
    BETA_STAR,
    CLASS_GREEN,
    TEST_PROFILE_DEPTH,
    TEST_TOWER_WINDOW,
    _frac_bin,
    biased_adversary_profile,
    build_summary,
    lean_wired,
    never_negative_profile,
    o_min_table,
    tower_census,
)


def test_o_min_table_matches_exact_comparison():
    table = o_min_table(80)
    pow2 = 1
    for k in range(1, 81):
        pow2 *= 2
        a = table[k]
        assert 3**a >= pow2
        assert a == 0 or 3 ** (a - 1) < pow2


def test_never_negative_count_matches_brute_force():
    d = 10
    brute = 0
    for word in range(1 << d):
        pow3, pow2, ok = 1, 1, True
        for i in range(d):
            if (word >> i) & 1:  # odd letter
                pow3 *= 3
            pow2 *= 2
            if pow3 < pow2:
                ok = False
                break
        brute += ok
    profile = never_negative_profile(d)
    row = next(r for r in profile["rows"] if r["d"] == d)
    assert row["count"] == brute


def test_profile_decreases_and_hoeffding_majorizes():
    profile = never_negative_profile(TEST_PROFILE_DEPTH)
    assert profile["monotone_decreasing"]
    assert profile["hoeffding_majorizes"]


def test_biased_adversary_matches_fair_coin_at_half():
    d = TEST_PROFILE_DEPTH
    fair = biased_adversary_profile(d, betas=(0.5,))["rows"][0]
    profile = never_negative_profile(d)
    row = next(r for r in profile["rows"] if r["d"] == d)
    assert abs(fair["survivor_measure"] - row["ratio"]) <= 1e-12
    # supercritical betas decay, and more bias decays faster
    rows = biased_adversary_profile(d, betas=(0.37, 0.45, 0.5))["rows"]
    measures = [r["survivor_measure"] for r in rows]
    assert all(m < 1.0 for m in measures)
    assert measures[0] > measures[1] > measures[2]
    assert 0.369 < BETA_STAR < 0.3691


def test_frac_bin_matches_high_precision():
    getcontext().prec = 80
    for n in (7, 100, 1023, 65537, 999999):
        cube = Decimal(n) ** 3
        frac = cube.sqrt() - int(cube.sqrt())
        assert _frac_bin(n, 8) == int(8 * frac)


def test_tower_census_small_window():
    census = tower_census(TEST_TOWER_WINDOW)
    assert census["samples"] > 0
    assert census["occupied_cells"] <= census["bins"] ** 3
    share = census["oooo_even_fifth_share"]
    assert share is None or 0.0 <= share <= 1.0


def test_lean_wired_and_anti_overclaim():
    assert all(lean_wired().values())
    assert not ANTI["k3_bound_claimed"]
    assert not ANTI["density_one_claimed"]
    assert not ANTI["toolkit_reopened"]
    assert not ANTI["paper_b_modified"]
    assert not ANTI["ergodic_theorem_claimed"]


def test_summary_classifies():
    summary = build_summary(d_max=TEST_PROFILE_DEPTH, n_max=200_000)
    assert summary["decision"]["classification"] == CLASS_GREEN
