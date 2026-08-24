"""Time-augmented quotients and accepting-slab layers. Finite checks are not proofs."""

from __future__ import annotations

import pytest

from research.ostrowski.exceptional_kernel import (
    affine_augmented_search,
    length_window_extended,
    time_augmented_row,
    time_augmented_search,
)
from research.ostrowski.live_layers import (
    REVERSE_BOX_NOT_A_PROOF,
    energy_canonical,
    extrema_report,
    forward_layers,
    layer_table,
    method_a_b_agree,
)
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.residual import residual_integer
from research.ostrowski.system import nonpisot_order3
from research.ostrowski.terminal_set import kernel_family_state


def test_energy_is_s1_qm2_plus_s2_qm1_plus_s3_qn():
    sys = nonpisot_order3()
    samples = (
        ((0, 0, 0), 5),
        ((1, -1, 0), 4),
        ((-3, -1, 0), 8),
        ((6, 5, 0), 3),
        ((2, -3, 1), 0),
    )
    for state, n in samples:
        explicit = (
            state[0] * sys.place_value(n - 2)
            + state[1] * sys.place_value(n - 1)
            + state[2] * sys.place_value(n)
        )
        assert energy_canonical(sys, state, n) == explicit
        assert energy_canonical(sys, state, n) == residual_integer(sys, state, n)


def test_time_augmented_quotients_do_not_separate():
    report = time_augmented_search((8, 9, 12, 18))
    assert report["any_separates"] is False
    assert report["finite_quotient_is_not_unreachability"]
    assert report["over_approx_interior_W"]
    by_m = {row["m"]: row for row in report["rows"]}
    assert by_m[8]["g_size"] == 4096
    assert by_m[8]["reachable"] == 4096
    assert by_m[9]["g_size"] == 6561
    assert by_m[9]["reachable"] == 729
    assert by_m[12]["g_size"] == 20736
    assert by_m[12]["reachable"] == 6912
    assert by_m[18]["g_size"] == 104976
    assert by_m[18]["reachable"] == 11664
    for row in report["rows"]:
        assert row["separates"] is False
        assert row["hits_0"] == row["target_0_count"]
        assert row["hits_12"] == row["target_12_count"]
        assert row["finite_quotient_hit_is_not_reachability"]


@pytest.mark.slow
def test_large_gm_also_collapse():
    expected = {
        24: (331776, 110592),
        27: (531441, 59049),
        36: (1679616, 186624),
        48: (5308416, 1769472),
    }
    for m, (g_size, reachable) in expected.items():
        row = time_augmented_row(m)
        assert row["g_size"] == g_size
        assert row["reachable"] == reachable
        assert row["separates"] is False
        assert row["hits_0"] == row["target_0_count"]
        assert row["hits_12"] == row["target_12_count"]


def test_affine_augmented_finds_no_new_separator():
    report = affine_augmented_search((8, 9, 12))
    assert report["count"] == 0
    assert report["separating_laws"] == []
    assert report["discarded_s1_and_time_reparams"]
    assert report["finite_quotient_is_not_unreachability"]


def test_length_window_hits_when_prefix_exists():
    report = length_window_extended((8, 9), 52)
    assert report["window_is_not_a_global_obstruction"]
    by_m = {row["m"]: row for row in report["rows"]}
    assert 24 in by_m[9]["class_0_residue_hits"]
    assert 48 in by_m[9]["class_0_residue_hits"]
    assert 12 in by_m[9]["class_12_residue_hits"]
    assert 36 in by_m[9]["class_12_residue_hits"]
    assert by_m[9]["class_0_residue_misses"] == []
    assert by_m[9]["class_12_residue_misses"] == []


def test_live_layers_from_start_12():
    sys = nonpisot_order3()
    fwd = forward_layers(sys, 12, live_only=True)
    rows = {n: fwd["layers"][n] for n in range(13)}
    assert rows[12]["R"] == 1 and rows[12]["L"] == 1
    assert rows[12]["s_max"] == (0, 0, 0)
    assert rows[10]["R"] == 9 and rows[10]["L"] == 9
    assert rows[10]["hub_in_L"]
    assert rows[10]["s_max"] == (-6, -2, 0)
    assert rows[0]["R"] == 165 and rows[0]["L"] == 165
    assert rows[0]["s_max"] == (-27, -6, 0)
    assert rows[0]["prefix"] == (2, -4, -4, 0, 0, -4, 1, 1, -4, 1, 1, -2)
    assert HUB in rows[10]["states_L"]
    for n, row in rows.items():
        assert row["R"] == row["L"]
        assert row["tn_in_L"] is False
        assert row["hub_in_L"] is (n <= 10)
        if n >= 1:
            assert kernel_family_state(sys, n) not in row["states_L"]


def test_legal_w_Rn_is_larger_than_Ln():
    rows = {row["n"]: row for row in layer_table(4, live_only=False)}
    assert rows[4]["R"] == rows[4]["L"] == 1
    assert rows[0]["R"] == 1192
    assert rows[0]["L"] == 10
    assert rows[0]["R"] > rows[0]["L"]
    assert rows[1]["R"] == 343 and rows[1]["L"] == 14


def test_method_a_b_agree_on_boxed_layers():
    for n in range(0, 5):
        report = method_a_b_agree(4, n, 6)
        assert report["agree"]
        assert report["finite_check_is_not_a_proof"]
        assert report[REVERSE_BOX_NOT_A_PROOF]
        assert report["only_in_forward"] == []
        assert report["only_in_reverse"] == []
    deep = method_a_b_agree(6, 0, 6)
    assert deep["agree"]
    assert deep["forward_L_in_box"] == 19
    assert deep["reverse_origin_hits"] == 19


def test_live_layers_n16_accepting_extrema():
    rows = {row["n"]: row for row in layer_table(16, live_only=True)}
    assert rows[16]["L"] == 1
    assert rows[0]["L"] == 379
    assert rows[0]["s_max"] == (-3, -37, 0)
    assert rows[1]["s_max"] == (-36, 0, 0)
    assert rows[0]["tn_in_L"] is False
    assert rows[0]["max_linf"] == 37
    assert rows[0]["s_max"] != (0, 0, 0)


def test_no_q_ansatz_and_no_infinitude_claim():
    report = extrema_report(12)
    assert report["q_ansatz"]["matched"] is False
    assert report["finite_depth_is_not_infinitude"]
    assert report["unbounded_K_does_not_imply_unbounded_L0"]
    assert report["kernel_family_is_not_the_only_probe"]
    assert report["functionals"]["observation_is_not_an_invariant"]
    assert report["spectral"]["not_a_spectral_theorem"]
    assert report["live_union_count"] == 532
