"""Exceptional kernel classes n ≡ 0, 12 (mod 24). Finite searches are not proofs."""

from __future__ import annotations

from research.ostrowski.exceptional_kernel import (
    REVERSE_NOT_A_PROOF,
    W_INTERIOR,
    class_target_residues,
    exceptional_ns,
    f_return_legal,
    f_return_report,
    affine_search,
    length_mod_search,
    modular_search,
    periodic_blocks,
    phase0_report,
    reverse_cones_exceptional,
    _q_period,
)
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.origin_live import q_mod3_period, q_mod9_period
from research.ostrowski.system import nonpisot_order3
from research.ostrowski.terminal_set import kernel_family_state


def test_exceptional_sequences_are_separate():
    assert exceptional_ns(0, 4) == (24, 48, 72, 96)
    assert exceptional_ns(12, 4) == (12, 36, 60, 84)
    assert set(exceptional_ns(0, 3)).isdisjoint(exceptional_ns(12, 3))


def test_q_period_matches_origin_live():
    assert _q_period(3) == q_mod3_period()
    assert _q_period(9) == q_mod9_period()


def test_mod9_classes_occupy_distinct_reachable_residues():
    t0 = class_target_residues(9, 0)
    t12 = class_target_residues(9, 12)
    assert t0 == frozenset({(6, 5, 0)})
    assert t12 == frozenset({(3, 4, 0)})
    assert t0.isdisjoint(t12)
    sys = nonpisot_order3()
    assert tuple(x % 9 for x in kernel_family_state(sys, 24)) == (6, 5, 0)
    assert tuple(x % 9 for x in kernel_family_state(sys, 12)) == (3, 4, 0)


def test_modular_search_does_not_separate_either_class():
    report = modular_search()
    assert report["any_separates_0_free"] is False
    assert report["any_separates_12_free"] is False
    assert report["any_separates_0_W"] is False
    assert report["any_separates_12_W"] is False
    by_m = {row["m"]: row for row in report["rows"]}
    assert by_m[9]["reachable_W"] == 81
    assert by_m[9]["reachable_free"] == 81
    assert by_m[4]["reachable_W"] == 64
    assert by_m[8]["reachable_W"] == 512
    assert by_m[27]["reachable_W"] == 2187
    assert by_m[27]["separates_0_free"] is False
    assert report["s1_mod3_is_not_a_new_invariant"]
    assert report["unbounded_K_does_not_imply_unbounded_L0"]


def test_affine_search_finds_no_new_separator():
    report = affine_search()
    assert report["count"] == 0
    assert report["separating_laws"] == []
    assert report["discarded_s1_reparams"]


def test_length_residues_are_not_a_global_obstruction():
    report = length_mod_search()
    assert report["window_is_not_a_global_obstruction"]
    by_m = {row["m"]: row for row in report["rows"]}
    assert 12 in by_m[9]["class_12_residue_hits"]
    assert by_m[9]["length_mod_is_not_OriginReachable"]


def test_reverse_cones_miss_origin_and_stay_huge():
    report = reverse_cones_exceptional()
    assert report["any_hit_origin"] is False
    assert report[REVERSE_NOT_A_PROOF]
    assert report["class_0_ns"] == [24, 48]
    assert report["class_12_ns"] == [12, 36]
    for row in report["rows"]:
        assert row["hit_origin"] is False
        assert row["min_l1"] > 57
        assert row[REVERSE_NOT_A_PROOF]
        assert row["C_of_zero_is_not_R_W"]


def test_f_return_ray_is_bounded_and_misses_tn():
    report = f_return_report()
    assert report["legal_k"] == [-2, -1, 0, 1]
    assert report["legal_k_bounded"]
    assert report["hub_on_ray"]
    assert report["kernel_family_not_on_ray"]
    assert report["bounded_ray_is_not_unbounded_L0"]
    assert f_return_legal(0, 0, 1) == HUB
    assert f_return_legal(0, 0, -4) is None
    for w in W_INTERIOR:
        image = f_return_legal(3, 1, w)
        if image is not None:
            assert image[0] == 3 * image[1]
            assert image[2] == 0


def test_periodic_blocks_do_not_hit_exceptional_tn():
    report = periodic_blocks()
    assert report["tn_hits"] == []
    assert report["growth_is_not_infinitude_of_L0"]
    assert report["tn_hit_requires_acceptance_too"]


def test_phase0_is_outcome_d_not_a_proof():
    report = phase0_report()
    assert report["closed_alphabet_free_obstruction"] is False
    assert report["closed_W_obstruction"] is False
    assert report["affine_alphabet_free_obstruction"] is False
    assert report["bridge_tn_found"] is False
    assert report["legal_two_step_ray_bounded"] is True
    assert report["any_cone_hit_origin"] is False
    assert report["outcome_d_no_theorem"]
    assert report["K_unbounded_does_not_imply_L0_unbounded"]
    assert report["tn_unreachability_does_not_imply_L0_finite"]
    assert report[REVERSE_NOT_A_PROOF]
