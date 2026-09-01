"""Horizontal Weyl species probe: unwind identities, first difference, wiring."""

from __future__ import annotations

from math import isqrt

from research.juggler_sequence.horizontal_weyl import (
    ANTI,
    BOUND_32,
    BOUND_34,
    BOUND_94,
    CLASS_GREEN,
    C_LEADING,
    ENGINE_LINE,
    build_summary,
    first_difference_check,
    floor_sqrt_diff,
    unwind_check,
)


# test-sized samples (the science list includes 10^12; too slow for the fast suite)
TEST_IDENTITY_SAMPLES = tuple(range(5, 201, 2)) + (10**4 + 1, 10**6 + 1)
TEST_LEMMA_G_SAMPLES = tuple(range(5, 201, 2)) + (10**6 + 1,)
TEST_DIFF_BLOCKS = ((10001, 10001 + 80),)


def test_floor_sqrt_diff_matches_isqrt_gap():
    for n in (5, 17, 1001, 99999, 10**6 + 1):
        a = (n + 2) ** 3
        b = n**3
        got = floor_sqrt_diff(a, b)
        # floor(sqrt(a))-floor(sqrt(b)) is Delta v; floor(sqrt(a)-sqrt(b))
        # is within {Delta v - 1, Delta v}
        dv = isqrt(a) - isqrt(b)
        assert got in (dv - 1, dv)
        assert got >= 0


def test_unwind_bounds_hold_on_small_samples():
    result = unwind_check(TEST_IDENTITY_SAMPLES)
    assert result["holds"]
    assert result["samples_used"] > 20
    assert result["worst_ratio_34"] <= BOUND_34 * (1.0 + 1e-4)
    assert result["worst_ratio_32"] <= BOUND_32 * (1.0 + 1e-4)
    assert result["worst_ratio_94_hi"] <= BOUND_94 * (1.0 + 1e-4)
    assert result["worst_ratio_94_lo"] >= BOUND_94 / (1.0 + 1e-4)


def test_first_difference_is_gg_below_engine():
    diff = first_difference_check(TEST_DIFF_BLOCKS)
    assert diff["mvt_holds"]
    assert diff["carry_holds"]
    assert diff["c_below_engine"]
    assert diff["c_exponent"] < ENGINE_LINE
    assert diff["cprime_gg"]
    assert diff["cprime_exponent"] > 0
    assert abs(diff["mean_c_over_n15"] - C_LEADING) < 0.05


def test_summary_green_and_anti_overclaim():
    summary = build_summary(
        identity_samples=TEST_IDENTITY_SAMPLES,
        lemma_g_samples=TEST_LEMMA_G_SAMPLES,
        diff_blocks=TEST_DIFF_BLOCKS,
    )
    assert summary["decision"]["classification"] == CLASS_GREEN
    assert summary["decision"]["shortcut_dead"]
    assert not summary["decision"]["falsifier_b"]
    assert summary["species"]["shortcut_dead"]
    assert summary["species"]["rate_free_target_unharmed"]
    axes = {a["axis"]: a for a in summary["species"]["axes"]}
    assert axes["v^{3/4}"]["reduction_lemma"]
    assert axes["v^{3/2}"]["reduction_lemma"]
    assert axes["v^{9/4}_unwind"]["species"] == "HH"
    assert axes["v^{9/4}_weyl1"]["species"] == "GG"
    assert not any(a["theorem_r_citable"] for a in summary["species"]["axes"])
    assert not ANTI["equidistribution_claimed"]
    assert not ANTI["k3_bound_claimed"]
    assert not ANTI["toolkit_reopened"]
    assert not ANTI["paper_b_modified"]
    assert not ANTI["theorem_r_cited_at_alpha_zero"]
    assert not ANTI["density_one_claimed"]
    assert summary["lemma_g"]["holds"]
