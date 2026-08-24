"""Accepting-boundary characterization: K_n, unbounded family, (30,25,0)."""

from __future__ import annotations

from research.ostrowski.exact_closure import basin_of_zero
from research.ostrowski.live_growth import reachable_live, unread_tail_bounds
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.residual import residual_integer
from research.ostrowski.residual_closure import B_MIN
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import nonpisot_order3, phase0_order3
from research.ostrowski.terminal_set import (
    SAMPLE_ACCEPTING,
    boxed_window_count,
    energy_on_f,
    hi_closed_form,
    hub_in_every_kn,
    is_terminal,
    kernel_family_is_terminal,
    kernel_family_state,
    kn_is_infinite_slab,
    last_step_lands_in_f,
    lo_closed_form,
    lsd_last_step_is_remaining_one_liveness,
    pisot_terminal_comparison,
    place_sum_at_most_twice_last,
    place_sum_bound_inductive,
    place_values_strictly_increasing,
    sample_accepting_only_at_remaining_zero,
    zero_seed_family_state,
)


def test_e0_is_s3_so_k0_is_the_plane_f():
    sys = nonpisot_order3()
    for s3 in (-4, -1, 0, 1, 7):
        assert residual_integer(sys, (9, -8, s3), 0) == s3
        assert is_terminal(sys, (9, -8, s3), 0) is (s3 == 0)
    assert is_terminal(sys, SAMPLE_ACCEPTING, 0)
    assert is_terminal(sys, (0, 0, 0), 0)
    assert not is_terminal(sys, (0, 0, 1), 0)


def test_singleton_zero_is_not_k():
    sys = nonpisot_order3()
    assert zero_seed_family_state(7) == (7, 0, 0)
    assert is_terminal(sys, (7, 0, 0), 0)
    assert (7, 0, 0) != (0, 0, 0)


def test_kernel_family_has_energy_zero_and_grows():
    sys = nonpisot_order3()
    prev_l1 = -1
    for n in range(1, 12):
        t = kernel_family_state(sys, n)
        assert t[2] == 0
        assert energy_on_f(sys, t[0], t[1], n) == 0
        assert kernel_family_is_terminal(sys, n)
        l1 = abs(t[0]) + abs(t[1])
        assert l1 > prev_l1
        prev_l1 = l1
    assert place_values_strictly_increasing(sys, 16)
    slab = kn_is_infinite_slab(sys, 5)
    assert slab["cardinality"] == "infinite"
    assert slab["plane_cardinality"] == "infinite"


def test_k_n_is_not_nested():
    sys = nonpisot_order3()
    assert is_terminal(sys, SAMPLE_ACCEPTING, 0)
    assert not is_terminal(sys, SAMPLE_ACCEPTING, 1)
    t = kernel_family_state(sys, 6)
    assert is_terminal(sys, t, 6)
    assert t[2] == 0
    # Large kernel point is in K_6 and not in the remaining-1 slab.
    assert not is_terminal(sys, t, 1)


def test_lo_hi_closed_forms_match_unread_tail_bounds():
    for sys in (nonpisot_order3(), phase0_order3()):
        for n in range(1, 10):
            lo, hi = unread_tail_bounds(sys, n)
            assert lo == lo_closed_form(sys, n)
            assert hi == hi_closed_form(sys, n)


def test_lsd_last_step_is_remaining_one_liveness():
    sys = nonpisot_order3()
    for state in ((0, 0, 0), (1, -1, 2), (15, -20, 10), HUB):
        assert lsd_last_step_is_remaining_one_liveness(sys, state)
    assert last_step_lands_in_f((15, -20, 10), 0)
    assert transition_affine(sys, (15, -20, 10), 0) == SAMPLE_ACCEPTING


def test_sample_accepting_only_at_remaining_zero():
    sys = nonpisot_order3()
    report = sample_accepting_only_at_remaining_zero(sys)
    assert report["only_remaining_zero"]
    assert report["in_K_0"]
    assert report["in_any_K_n_for_n_ge_1"] is False
    assert report["live_remaining_lengths"] == (0,)
    assert place_sum_at_most_twice_last(sys, 20)
    assert place_sum_bound_inductive(sys)
    assert SAMPLE_ACCEPTING not in basin_of_zero()["states"]


def test_hub_is_bounded_point_of_every_kn_on_f():
    sys = nonpisot_order3()
    assert HUB[2] == 0
    assert hub_in_every_kn(sys, 20)
    assert HUB in basin_of_zero()["states"]


def test_boxed_window_is_not_cardinality_of_kn():
    sys = nonpisot_order3()
    win = boxed_window_count(sys, 0, 4)
    assert win["window_count"] == 81
    assert win["window_plane_count"] == 81
    win1 = boxed_window_count(sys, 1, 4)
    assert win1["window_count"] == 162
    # Finite window of an infinite set.
    assert kn_is_infinite_slab(sys, 1)["cardinality"] == "infinite"


def test_pisot_control_has_same_k0_and_finite_reachable_terminals():
    cmp = pisot_terminal_comparison()
    assert cmp["control_K_0_is_F"]
    assert cmp["np_K_0_is_F"]
    assert cmp["b_min_cardinality"] == 55
    assert cmp["b_min_in_F"] == 18
    assert len(B_MIN) == 55
    assert reachable_live(phase0_order3(), 12)["states"] == B_MIN
    # Same terminal predicate; different reachable live set.
    sys_np = nonpisot_order3()
    assert is_terminal(sys_np, SAMPLE_ACCEPTING, 0)
    assert SAMPLE_ACCEPTING not in B_MIN
