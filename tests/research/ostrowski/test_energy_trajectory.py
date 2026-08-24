"""Telescoping unread-tail energy, defects, and energy-compatible blocks.

The telescope is KNOWN packaging of ``energy_step``, not an ``L_0`` bound.
``K_n`` is normalized control of ``E_n``, not coordinate boundedness.
Finite-depth expanding blocks are not infinitude.
"""

from __future__ import annotations

from research.ostrowski.energy_geometry import energy_step_identity
from research.ostrowski.energy_trajectory import (
    EXACT_LO_HI,
    GROWTH_NOT_INFINITUDE,
    NORMALIZED_NOT_COORDINATE,
    ORIGIN,
    apply_word,
    consumed_sum,
    defect_minus_after_step,
    defect_plus_after_step,
    energy_after_word,
    energy_compatible_blocks,
    energy_telescope_holds,
    energy_telescope_rhs,
    interpretation_sample,
    large_s3_ratios,
    lo_hi_ratio_bounds,
    remaining_one_form,
    remaining_one_slab,
    wmax_at_place,
    wmin_at_place,
)
from research.ostrowski.live_layers import energy_canonical
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import nonpisot_order3
from research.ostrowski.terminal_set import hi_closed_form, lo_closed_form, is_terminal


def test_telescope_matches_iterated_energy_step():
    sys = nonpisot_order3()
    words = ((1,), (1, -2), (2, -4, 0, 1), tuple(range(-4, 3)))
    starts = ((0, 0, 0), (-3, -1, 0), (6, 5, 1))
    for start in starts:
        for word in words:
            n = len(word) + 3
            assert energy_telescope_holds(sys, n, word, start)
            state = start
            rem = n
            for w in word:
                assert energy_step_identity(sys, state, w, rem)
                state = transition_affine(sys, state, w)
                rem -= 1
            assert energy_canonical(sys, state, rem) == energy_telescope_rhs(
                sys, n, word, start
            )
    assert energy_telescope_holds(sys, 5, (), ORIGIN)


def test_origin_energy_is_minus_consumed():
    sys = nonpisot_order3()
    word = (2, -4, 0, 1)
    n = 6
    assert energy_canonical(sys, ORIGIN, n) == 0
    assert energy_after_word(sys, n, word) == -consumed_sum(sys, n, word)
    assert energy_after_word(sys, n, word) == energy_telescope_rhs(sys, n, word)


def test_interpretation_difference_words():
    report = interpretation_sample()
    assert len(report["samples"]) == 2
    ok, miss = report["samples"]
    assert ok["w_msd"] == (0, 1, -2)
    assert ok["accepts"] and ok["value_identity"]
    assert miss["w_msd"] == (0, 0, -2)
    assert not miss["accepts"] and not miss["value_identity"]
    for sample in report["samples"]:
        assert sample["telescope"]
        assert sample["matches_residual_run"]
        assert sample["E_0"] == sample["minus_consumed"] == sample["s3"]
        assert sample["E_0_eq_s3"]
        assert sample["accept_iff_sum_zero"]


def test_lo_hi_closed_forms_and_ratio_bounds():
    sys = nonpisot_order3()
    for n, qn, s_nm1, lo, hi in EXACT_LO_HI:
        row = lo_hi_ratio_bounds(sys, n)
        assert row["qn"] == qn
        assert row["S_nm1"] == s_nm1
        assert row["lo"] == lo == lo_closed_form(sys, n)
        assert row["hi"] == hi == hi_closed_form(sys, n)
        assert row["matches_unread"]
        assert row["S_le_two_qnm1"]
        assert row["qn_ge_two_qnm1"]
        assert row["hi_over_qn_lt_2"]
        assert row["lo_over_qn_gt_minus_4"]
        assert row[NORMALIZED_NOT_COORDINATE]
        if n >= 2:
            assert -4 < lo / qn < hi / qn < 2


def test_defect_step_identity():
    sys = nonpisot_order3()
    states = ((0, 0, 0), (-3, -1, 0), (6, 5, 1), (2, -7, 3))
    for remaining in (1, 2, 5, 8):
        alph = range(wmin_at_place(remaining - 1), wmax_at_place(remaining - 1) + 1)
        for state in states:
            for w in alph:
                plus_l, plus_r = defect_plus_after_step(sys, state, w, remaining)
                minus_l, minus_r = defect_minus_after_step(sys, state, w, remaining)
                assert plus_l == plus_r
                assert minus_l == minus_r


def test_remaining_one_form_is_length_dependent_slab():
    lo, hi = remaining_one_slab()
    assert (lo, hi) == (-2, 1)
    assert remaining_one_form((0, 0, 0)) == 0
    assert remaining_one_form((-3, -37, 19)) == 1
    # Length-dependent: every live state at remaining 1 obeys this, not a global L_0 bound.
    assert lo <= remaining_one_form((-3, -37, 19)) <= hi


def test_kn_flag_is_normalized_not_coordinate():
    sys = nonpisot_order3()
    # Live at remaining 1 can have large coordinates while E_1 stays in [-2, 1].
    assert remaining_one_form((-3, -37, 19)) == 1
    assert is_terminal(sys, (-3, -37, 19), 1)
    row = lo_hi_ratio_bounds(sys, 8)
    assert row[NORMALIZED_NOT_COORDINATE]


def test_large_s3_slice_ratios_are_not_the_eigen_ray():
    report = large_s3_ratios(20)
    assert report["is_slice_not_union"]
    assert report["floats_are_classification_only"]
    assert report["remaining_one_all_in_slab"]
    assert report["remaining_one_is_length_dependent"]
    assert report[GROWTH_NOT_INFINITUDE]
    assert report[NORMALIZED_NOT_COORDINATE]
    by_n = {row["n"]: row for row in report["rows"]}
    assert by_n[1]["s"] == (-3, -37, 19)
    assert by_n[1]["L"] == 958
    assert by_n[2]["s"] == (21, 22, -15)
    assert by_n[2]["L"] == 1185
    assert by_n[3]["s"] == (9, 27, -12)
    assert by_n[3]["L"] == 1037
    eigen = report["eigen"]
    # Off the expanding eigen-direction by O(1); no family from this slice.
    for n in (1, 2, 3):
        assert abs(by_n[n]["s1_over_s3"] - eigen["s1_over_s3"]) > 1.0
        assert abs(by_n[n]["s2_over_s3"] - eigen["s2_over_s3"]) > 1.0


def test_expanding_blocks_leave_kn_zero_block_stays_bounded():
    report = energy_compatible_blocks()
    assert report["has_unbounded_live_family"] is False
    assert report["expanding_without_Kn_is_not_live"]
    assert report[GROWTH_NOT_INFINITUDE]
    assert report["live_hit_blocks"] == [(0,), (0, 0), (0, 0, 0)]
    assert report["bounded_live"] == 3
    assert report["live_growing_sample"] == []
    dead = report["expanding_not_in_K_sample"]
    assert dead
    assert dead[0]["block"] == (-4,)
    assert dead[0]["grew"]
    assert not dead[0]["live_all_repeats"]
    sys = nonpisot_order3()
    # Explicit expanding witness that is not in K at the matching remaining.
    orbit = apply_word(sys, ORIGIN, (-4,) * 4)
    assert not is_terminal(sys, orbit, 12 - 4)
