"""Unread-tail energy identity and length-independent live-form search.

The energy step is KNOWN construction covariance, not an ``L_0`` bound.
Finite horizon growth is not infinitude.
"""

from __future__ import annotations

from research.ostrowski.energy_geometry import (
    adjoint_covariance,
    compare_horizons,
    energy_step_identity,
    length_independent_combinations,
    method_a_b_agree,
    normalized_cone,
    normalized_energy_on_live,
    scan_integer_forms,
)
from research.ostrowski.live_layers import REVERSE_BOX_NOT_A_PROOF, energy_canonical
from research.ostrowski.system import nonpisot_order3


def test_adjoint_and_energy_step_including_underflow():
    sys = nonpisot_order3()
    for i in range(1, 16):
        assert adjoint_covariance(sys, i)
    samples = (
        ((0, 0, 0), 0, 1),
        ((0, 0, 0), 1, 1),
        ((2, -3, 1), -4, 1),
        ((-3, -1, 0), 2, 2),
        ((6, 5, 0), -2, 3),
        ((1, -7, 4), 2, 8),
        ((-9, 3, 2), -3, 12),
    )
    for state, w, i in samples:
        assert energy_step_identity(sys, state, w, i)
        image_e = energy_canonical(
            sys,
            (
                3 * state[2],
                state[0] + state[2],
                state[1] + 2 * state[2] - w,
            ),
            i - 1,
        )
        rhs = energy_canonical(sys, state, i) - w * sys.place_value(i - 1)
        assert image_e == rhs


def test_energy_zero_is_s3():
    sys = nonpisot_order3()
    assert energy_canonical(sys, (4, -5, 7), 0) == 7


def test_no_length_independent_three_energy_combination():
    report = length_independent_combinations()
    assert report["count"] == 0
    assert report["length_independent"] == []
    assert report["known_construction_not_L0"]


def test_normalized_energy_restates_the_slab():
    report = normalized_energy_on_live(8)
    assert report["all_inside_slab"]
    assert report["restates_Kn_not_origin_invariant"]


def test_all_small_integer_forms_grow_from_16_to_20():
    cmp = compare_horizons(16, 20)
    assert cmp["s3_grows"]
    assert cmp["small"]["coord_max"] == (36, 37, 12)
    assert cmp["large"]["coord_max"] == (57, 49, 19)
    assert cmp["small"]["live_union_count"] == 1351
    assert cmp["large"]["live_union_count"] == 2970
    for row in cmp["growth"]:
        assert row["grows"]
        assert row["counterexample_not_invariant"]
    s3 = next(g for g in cmp["growth"] if g["coeff"] == (0, 0, 1))
    assert s3["max_at_small"] == 12
    assert s3["max_at_large"] == 19
    scan = scan_integer_forms(cmp["_small_states"], cmp["_large_states"])
    assert scan["stable_count"] == 0
    assert scan["growing_count"] == 342
    assert scan["observation_is_not_an_invariant"]
    cone = normalized_cone(cmp["_large_states"])
    assert cone["occupies_both_sides"] == [True, True, True]
    assert cone["numerical_cone_is_not_a_theorem"]
    assert cmp["finite_depth_is_not_infinitude"]
    assert cmp["unbounded_K_does_not_imply_unbounded_L0"]


def test_method_a_b_still_agrees():
    report = method_a_b_agree(6, 0, 6)
    assert report["agree"]
    assert report[REVERSE_BOX_NOT_A_PROOF]
