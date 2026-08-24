"""Origin-reachable live set versus the kernel family t_n."""

from __future__ import annotations

from research.ostrowski.live_growth import reachable_live
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.origin_live import (
    forward_forces_s1_divisible_by_3,
    kernel_family_blocked_at_first_reverse,
    kernel_family_compatible_with_s1_mod3,
    kernel_family_reachability_report,
    kernel_family_s1_mod3,
    live_scan,
    origin_reachable_implies_s1_mod3_zero,
    pisot_has_no_s1_mod3_trap,
    q_mod3_period,
    q_mod9_period,
    q_mod_period,
    reverse_cone_hits_origin,
    two_step_f_to_f,
)
from research.ostrowski.residual_closure import B_MIN
from research.ostrowski.system import nonpisot_order3, phase0_order3
from research.ostrowski.terminal_set import kernel_family_state


def test_q_n_mod3_has_period_8():
    period = q_mod3_period()
    assert period == (1, 2, 2, 0, 2, 1, 1, 0)
    sys = nonpisot_order3()
    for i in range(40):
        assert sys.place_value(i) % 3 == period[i % 8]


def test_q_n_mod9_is_periodic():
    period = q_mod9_period()
    sys = nonpisot_order3()
    assert len(period) == 24
    for i in range(48):
        assert sys.place_value(i) % 9 == period[i % 24]
    assert q_mod_period(sys, 3) == q_mod3_period()


def test_every_np_image_has_s1_divisible_by_3():
    for state in ((0, 0, 0), (1, -1, 2), (-3, -1, 0), (6, 2, 1)):
        for w in range(-4, 3):
            assert forward_forces_s1_divisible_by_3(state, w)
    assert origin_reachable_implies_s1_mod3_zero((0, 0, 0))
    assert origin_reachable_implies_s1_mod3_zero((15, -5, 0))
    assert not origin_reachable_implies_s1_mod3_zero((1, 0, 0))


def test_lean_obstruction_table_n_1_to_48():
    """Python table matching Lean `kernel_unreachable_of_not_exceptional`."""
    sys = nonpisot_order3()
    rows = []
    open_n = []
    for n in range(1, 49):
        q_nm1_mod3 = sys.place_value(n - 1) % 3
        blocked = kernel_family_blocked_at_first_reverse(n)
        lean_hmod = not (n % 24 == 0 or n % 24 == 12)
        rows.append((n, q_nm1_mod3, blocked))
        if lean_hmod:
            assert blocked
        else:
            assert not blocked
            open_n.append(n)
        assert (q_nm1_mod3 == 0) is (n % 4 == 0)
    assert len(rows) == 48
    assert open_n == [12, 24, 36, 48]
    assert 12 in open_n and 24 in open_n and 36 in open_n
    report = kernel_family_reachability_report(36)
    assert report["open_n"] == [12, 24, 36]
    assert report["open_n_are_0_or_12_mod_24"]


def test_kernel_family_blocked_except_0_or_12_mod_24():
    report = kernel_family_reachability_report(24)
    assert report["open_n"] == [12, 24]
    assert report["open_n_are_0_or_12_mod_24"]
    assert report["unbounded_K_does_not_imply_unbounded_L0"]
    for n in range(1, 25):
        t = kernel_family_state(nonpisot_order3(), n)
        ok = kernel_family_compatible_with_s1_mod3(n)
        assert (t[0] % 3 == 0) is ok
        assert ok is (n % 4 == 0)
        if n % 24 not in (0, 12):
            assert kernel_family_blocked_at_first_reverse(n)
        if not ok:
            assert kernel_family_s1_mod3(n) != 0


def test_two_step_on_f_lands_on_the_ray():
    image = two_step_f_to_f(4, 1, -2, 4 + 2 * (1 - (-2)))
    assert image == (9, 3, 0)
    assert two_step_f_to_f(4, 1, 0, 0) is None


def test_reverse_cone_of_blocked_tn_misses_origin():
    sys = nonpisot_order3()
    for n in (1, 2, 4, 8):
        cone = reverse_cone_hits_origin(kernel_family_state(sys, n), 5)
        assert cone["hit_origin"] is False
    # Remaining arithmetic progression: reverse stays huge, not origin.
    cone12 = reverse_cone_hits_origin(kernel_family_state(sys, 12), 4)
    assert cone12["hit_origin"] is False
    assert cone12["min_l1"] > 0


def test_live_scan_obeys_s1_mod3_and_misses_tn():
    scan = live_scan(12)
    assert scan["all_s1_mod3_zero"]
    assert scan["kernel_family_hits"] == []
    assert scan["hub_in_L"]
    assert scan["finite_depth_is_not_infinitude"]
    R = reachable_live(nonpisot_order3(), 12)["states"]
    assert all(s[0] % 3 == 0 for s in R)
    assert HUB in R


def test_pisot_control_does_not_force_s1_mod3():
    cmp = pisot_has_no_s1_mod3_trap()
    assert cmp["occupies_all_three_classes"]
    assert set(s[0] % 3 for s in B_MIN) == {0, 1, 2}
    assert reachable_live(phase0_order3(), 12)["states"] == B_MIN
    assert len(B_MIN) == 55
