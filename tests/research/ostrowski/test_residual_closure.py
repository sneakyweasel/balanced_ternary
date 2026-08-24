"""Theorem-phase tests: live residual closure for the fixed order-3 Γ."""

from __future__ import annotations

from research.ostrowski.counterexample_search import find_escape, scan_escapes
from research.ostrowski.invariant_search import (
    compare_box_to_reach,
    deadness_certificate,
    exterior_images,
    verify_invariant,
)
from research.ostrowski.minimize import boxed_graph
from research.ostrowski.residual import next_state
from research.ostrowski.residual_closure import B_MIN, reachable_live
from research.ostrowski.system import phase0_order3
from research.ostrowski.transition_extremals import (
    INTERIOR_W,
    LSD_W,
    is_sign_flip_symmetry,
    legal_w,
    order3_transition,
    unread_tail_bounds,
)


def test_specialized_map_matches_general_transition():
    sys = phase0_order3()
    for state in ((0, 0, 0), (1, -1, 2), (-2, 3, -1)):
        for w in INTERIOR_W:
            assert order3_transition(state, w) == next_state(sys, state, w, 8)


def test_legal_w_is_the_section_5_3_alphabet():
    assert legal_w(0) == LSD_W == (-2, -1, 0, 1)
    assert legal_w(1) == INTERIOR_W == tuple(range(-4, 3))
    assert not is_sign_flip_symmetry()


def test_unread_tail_bounds_use_lsd_and_interior():
    assert unread_tail_bounds(0) == (0, 0)
    assert unread_tail_bounds(1) == (-2, 1)
    lo, hi = unread_tail_bounds(2)
    # q=(1,2): min -2*1 + -4*2 = -10; max 1*1 + 2*2 = 5
    assert (lo, hi) == (-10, 5)


def test_b_min_is_exactly_the_live_reachable_set():
    assert len(B_MIN) == 55
    assert (0, 0, 0) in B_MIN
    for length in (9, 12, 16):
        report = reachable_live(length)
        assert report["states"] == B_MIN
        assert report["max_abs_s3"] == 2
        assert report["states_with_abs_s3_ge_3"] == 0


def test_no_live_escape_with_abs_s3_above_two():
    scan = scan_escapes(12, s3_bound=2)
    assert scan["any_escape"] is False
    assert find_escape(12)["found"] is False


def test_b_min_is_live_invariant_at_several_remaining_lengths():
    for remaining in (1, 2, 5, 8, 12):
        check = verify_invariant(B_MIN, remaining)
        assert check["invariant"]
        assert check["leak_count"] == 0


def test_exterior_deadness_certificate():
    cert = deadness_certificate(B_MIN)
    assert cert["exterior_count"] == 108
    assert cert["overflow_initial_ok"]
    assert cert["underflow_initial_ok"]
    assert cert["recurrences_ok"]
    assert cert["proved"]
    ext = exterior_images(B_MIN)
    assert len(ext) == 108
    assert ext.isdisjoint(B_MIN)


def test_axis_box_strictly_contains_b_min():
    cmp = compare_box_to_reach(12, 2, 3, 2)
    assert cmp["reach_equals_b_min"]
    assert cmp["reach_subset_of_box"]
    assert cmp["box_not_reached"] > 0
    assert cmp["max_abs"] == (2, 3, 2)


def test_phase0_85_set_is_b_min_plus_never_live_states():
    raw, _delta = boxed_graph(phase0_order3(), 2, range(-4, 3))
    extra = set(raw) - set(B_MIN)
    assert len(raw) == 85
    assert B_MIN <= set(raw)
    assert len(extra) == 30
    from research.ostrowski.transition_extremals import residual_is_live

    assert not any(residual_is_live(state, i) for state in extra for i in range(13))
