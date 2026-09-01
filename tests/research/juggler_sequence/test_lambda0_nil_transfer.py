"""Lambda-0 nil-transfer probe: shifted Mal'cev, free fiber, JJ dictionary."""

from __future__ import annotations

from fractions import Fraction
from math import floor

from research.juggler_sequence.lambda0_nil_transfer import (
    ANTI,
    CLASS_CLOSED,
    TEST_TYPICALITY_BLOCKS,
    TEST_TYPICALITY_LAMBDAS,
    TEST_TYPICALITY_P,
    build_summary,
    identity_section,
    jj_dictionary,
    shifted_malcev_check,
    shifted_malcev_pair,
    typicality_witness,
)


def test_shifted_malcev_exact():
    for a, b, lam in (
        (Fraction(37, 13), Fraction(155, 17), Fraction(0)),
        (Fraction(3, 2), Fraction(9, 4), Fraction(1, 3)),
        (Fraction(-5, 2), Fraction(11, 7), Fraction(4, 9)),
    ):
        d = shifted_malcev_pair(a, b, lam)
        assert d["lhs"] == d["rhs"]
        assert d["lhs"] == d["abelian"] + d["vertical"]
        assert d["vertical"] == -a * floor(b + lam)


def test_shifted_malcev_check_passes():
    r = shifted_malcev_check()
    assert r["exact_identity"]
    assert r["scaled_identity"]
    assert r["scaled_gap"] == 0


def test_identity_section_is_free_fiber():
    s = identity_section()
    assert s["tower_parabola_exact_algebra"]
    assert s["pure_parabola_exact_algebra"]
    assert s["tower_scaled_ok"]
    assert s["pure_scaled_ok"]
    assert s["fiber_type"] == "free_center_fiber"
    assert s["lambda0_special"] is False
    assert s["character_sample"]["no_constant_character"]


def test_jj_dictionary_all_survive():
    d = jj_dictionary()
    assert d["all_survive"]
    assert d["new_average"] is False
    assert d["new_scale"] is False
    for clause in ("i", "ii", "iii"):
        assert d[clause]["verdict"] == "survives"


def test_typicality_witness_not_a_transfer():
    t = typicality_witness(
        TEST_TYPICALITY_P,
        n_lambda=TEST_TYPICALITY_LAMBDAS,
        n_blocks=TEST_TYPICALITY_BLOCKS,
    )
    assert t["typicality_is_not_a_transfer"]
    assert t["typical"]
    assert t["mean_abs_S0_over_sqrt_L"] < 4.0
    assert 0 < t["median_rank_of_S0_among_grid"] <= TEST_TYPICALITY_LAMBDAS


def test_summary_closes_reopen_and_anti_overclaim():
    summary = build_summary(
        p_block=TEST_TYPICALITY_P,
        n_lambda=TEST_TYPICALITY_LAMBDAS,
        n_blocks=TEST_TYPICALITY_BLOCKS,
    )
    assert summary["decision"]["classification"] == CLASS_CLOSED
    assert summary["decision"]["reopen"] == "CLOSE"
    assert summary["decision"]["v_hh_status"] == "PARKED"
    assert not summary["decision"]["new_average"]
    assert not ANTI["k3_bound_claimed"]
    assert not ANTI["hh_proved"]
    assert not ANTI["lambda0_transferred"]
    assert not ANTI["toolkit_reopened"]
    assert not ANTI["paper_b_modified"]
    assert ANTI["typicality_is_not_a_transfer"]
