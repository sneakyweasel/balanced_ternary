"""Reverse map, contraction certificate, and basin-versus-adder distinction."""

from __future__ import annotations

from fractions import Fraction

from research.ostrowski.contraction_certificate import (
    APRIORI_AXIS_BOUND,
    a_priori_preimage_bound,
    contraction_certificate,
    is_spd,
)
from research.ostrowski.exact_closure import (
    BASIN_EXTREMA,
    BASIN_FINGERPRINT,
    BASIN_MAX_L1,
    BASIN_MAX_Q_NORM_SQUARED,
    BASIN_OF_ZERO_CARDINALITY,
    BASIN_STABILIZATION_DEPTH,
    PARADOX_AT,
    basin_of_zero,
    canonical_basin_states,
    check_a_every_state_can_step_toward_origin,
    check_b_no_extra_preimage,
    compare_forward_to_basin,
    seed_justification,
)
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.reverse_map import (
    integer_preimage,
    inverse_times_forward_is_identity,
    np_inverse_matrix,
    reverse_matches_forward,
)
from research.ostrowski.residual_closure import B_MIN
from research.ostrowski.system import nonpisot_order3, phase0_order3


def test_inverse_times_forward_is_identity():
    assert inverse_times_forward_is_identity()
    inv = np_inverse_matrix()
    assert inv[0][0] == Fraction(-1, 3)
    assert inv[1][0] == Fraction(-2, 3)
    assert inv[2][0] == Fraction(1, 3)


def test_integer_reverse_inverts_forward():
    sys = nonpisot_order3()
    for state in ((0, 0, 0), (1, -1, 2), (-3, -1, 0), (6, 2, 0)):
        for w in range(-4, 3):
            assert reverse_matches_forward(sys, state, w)
    assert integer_preimage((1, 0, 0), 0) is None
    assert integer_preimage((3, 1, 0), 0) == (0, -2, 1)


def test_q_norm_contraction_certificate_is_exact():
    cert = contraction_certificate()
    assert cert["Q_spd"]
    assert cert["decrement_spd"]
    assert cert["mu_gap_spd"]
    assert cert["rho_gap_spd"]
    assert cert["rho_squared"] == Fraction(49, 50)
    assert cert["proved"]
    assert is_spd(cert["Q"])
    assert cert["Q_minors"] == (Fraction(10), Fraction(101), Fraction(457))


def test_apriori_preimage_box_is_exact_and_not_a_forward_bound():
    bound = a_priori_preimage_bound()
    assert bound["proved"]
    assert bound["apriori_axis_bound"] == APRIORI_AXIS_BOUND
    assert bound["applies_to_forward_images_of_origin"] is False
    assert bound["enumerating_the_box_is_not_the_proof"]


def test_basin_of_zero_is_finite_and_not_the_adder_live_set():
    report = basin_of_zero()
    assert report["cardinality"] == BASIN_OF_ZERO_CARDINALITY
    assert report["stabilization_depth"] == BASIN_STABILIZATION_DEPTH
    assert report["extrema"] == BASIN_EXTREMA
    assert report["max_l1"] == BASIN_MAX_L1
    assert report["max_q_norm_squared"] == BASIN_MAX_Q_NORM_SQUARED
    assert report["fingerprint"] == BASIN_FINGERPRINT
    assert report["origin_in_basin"]
    assert report["hub_in_basin"]
    assert report["sample_outside_adder_terminal"]
    assert report["inside_apriori_box"]
    assert (30, 25, 0) not in report["states"]
    assert HUB in report["states"]
    canonical = canonical_basin_states()
    assert len(canonical) == BASIN_OF_ZERO_CARDINALITY
    assert canonical[0] == (-33, -7, 5)
    assert canonical[-1] == (32, -1, -3)


def test_basin_fixed_point_checks():
    states = basin_of_zero()["states"]
    assert check_a_every_state_can_step_toward_origin(states)
    assert check_b_no_extra_preimage(states)


def test_forward_live_set_escapes_the_basin():
    cmp = compare_forward_to_basin(10)
    rec = PARADOX_AT[10]
    assert cmp["R_subset_of_basin"] is False
    assert cmp["R_minus_basin_count"] == rec["outside_basin"]
    assert cmp["finite_depth_is_not_infinitude"]
    assert cmp["hub_in_both"]
    assert cmp["R_still_inside_apriori_box"]
    last = cmp["table"][-1]
    assert last["live_states"] == rec["live_states"]
    assert last["outside_basin"] == rec["outside_basin"]


def test_depth_growth_is_not_infinitude_and_exits_computed_basin():
    from research.ostrowski.live_growth import growth_table

    rec = PARADOX_AT[16]
    row = growth_table(nonpisot_order3(), 16)[-1]
    assert row["live_states"] == rec["live_states"]
    assert row["new_live_states"] > 0
    max_abs = (row["max_abs_s1"], row["max_abs_s2"], row["max_abs_s3"])
    assert max_abs == rec["max_abs"]
    # Depth 16 leaves the computed C({0}) axis box, not the crude Lyapunov box.
    assert row["max_abs_s2"] > max(abs(BASIN_EXTREMA[1][0]), abs(BASIN_EXTREMA[1][1]))
    assert max(max_abs) < APRIORI_AXIS_BOUND


def test_accepting_slice_is_not_a_finite_seed():
    just = seed_justification()
    assert just["F_finite"] is False
    assert just["C_of_F_bounded_by_reverse_contraction"] is False
    assert just["C_of_zero_is_not_adder_live_set"] is True
    assert just["honest_finite_seed"] == ((0, 0, 0),)


def test_pisot_control_is_still_55():
    from research.ostrowski.live_growth import reachable_live

    assert reachable_live(phase0_order3(), 12)["states"] == B_MIN
    assert len(B_MIN) == 55
