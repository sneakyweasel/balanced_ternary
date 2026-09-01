"""Horizontal Weyl catalog: axis reductions and defect witnesses."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

from research.juggler_sequence.nil_horizontal_weyl import (
    ANTI,
    CLASS_SPLIT,
    COEF_34_THETA,
    COEF_94_THETA,
    COEF_N27,
    COEF_N98,
    TEST_SAMPLES,
    axis_catalog,
    build_summary,
    coefficient_identities,
    defect_witnesses,
    drift_arithmetic,
    integer_harmonic_identity,
)
from research.juggler_sequence.two_step_parity import second_order_scan


def test_lemma_g_coefficients_after_substitution():
    assert COEF_N27 == 1
    assert COEF_N98 == 1
    assert COEF_94_THETA == -Fraction(9, 4)
    assert COEF_34_THETA == -Fraction(3, 4)
    ids = coefficient_identities()
    assert ids["holds"]


def test_drift_exponents_are_exact():
    d = drift_arithmetic()
    assert d["alpha"] == "15/8"
    assert d["engine_line"] == "9/4"
    assert d["w_family_cap"] == "9/8"
    assert d["below_engine"]
    assert d["above_w_family_cap"]
    assert d["layer"] == "first"
    assert d["gg_reenters_n_reduction"]
    assert not d["bb_applies"]
    assert d["per_step_prefactor"] == "135/16"
    assert d["window_prefactor"] == "32/135"
    assert d["named_bound"] is None


def test_integer_harmonic_on_test_samples():
    result = integer_harmonic_identity(TEST_SAMPLES)
    assert result["holds"]
    assert result["checked"] == len([n for n in TEST_SAMPLES if n % 2 == 1])


def test_integer_harmonic_is_algebra():
    # k2 * v^{3/2} - k2 * {v^{3/2}} = k2 * floor(v^{3/2}) is an integer.
    for n in (11, 101, 10001):
        v = isqrt(n * n * n)
        # floor(v^{3/2}) = isqrt(v^3)
        fl = isqrt(v * v * v)
        for k2 in (-2, 1, 2):
            assert k2 * fl == int(k2 * fl)


def test_lemma_g_still_holds_on_test_samples():
    assert second_order_scan(TEST_SAMPLES)["holds"] is True


def test_defect_witnesses_on_test_samples():
    result = defect_witnesses(TEST_SAMPLES)
    assert result["used"] >= 3
    assert result["holds"]
    assert result["nine_fourths_not_remainder"]
    assert result["three_fourths_decays"]
    assert abs(result["ratio_94_min"] - 1.0) <= 0.05
    assert abs(result["ratio_94_max"] - 1.0) <= 0.05


def test_catalog_splits_the_axes():
    cat = axis_catalog()
    assert cat["axis_32"]["class"] == "THEOREM_C_SUBSTRATE"
    assert cat["axis_32"]["already_a_theorem"] is False
    assert cat["axis_34"]["already_a_theorem"] is True
    assert cat["axis_94"]["already_a_theorem"] is False
    assert cat["axis_94"]["gg_reenters_n_reduction"] is True
    assert cat["mixed"]["inherits_94_leftover"] is True
    assert cat["horizontal_half_already_a_theorem"] is False


def test_summary_close_and_anti_overclaim():
    summary = build_summary(samples=TEST_SAMPLES)
    assert summary["decision"]["classification"] == CLASS_SPLIT
    assert summary["decision"]["branch"] == "CLOSE"
    assert summary["decision"]["already_a_theorem"] is False
    assert not ANTI["equidistribution_claimed"]
    assert not ANTI["k3_bound_claimed"]
    assert not ANTI["toolkit_reopened"]
    assert not ANTI["paper_b_modified"]
    assert not ANTI["horizontal_half_already_a_theorem"]
