"""Local uniqueness is not global N_k constancy."""

from __future__ import annotations

from research.stabilization.triage import local_vs_global_report, witness_mixed_clusters


def test_witness_splits_a_hensel_node_from_a_moving_count():
    rec = witness_mixed_clusters(5)
    assert rec["simple_node"]["singular"] is False
    assert rec["simple_node"]["children"] == 1
    assert rec["simple_node"]["unique_lift_thereafter"]
    assert rec["cluster_node"]["singular"] is True
    assert rec["N_k_constant_from_level_1"] is False
    assert rec["local_unique_but_global_moving"]
    assert rec["N_k"][0] == 1
    assert rec["N_k"][1] == 2
    assert rec["N_k"][2] != rec["N_k"][1] or rec["N_k"][3] != rec["N_k"][1]


def test_triage_verdict_is_no_novelty():
    report = local_vs_global_report(4)
    verdict = report["verdict"]
    assert verdict["k0_is_a_closed_form_for_N_k"]
    assert verdict["k0_is_not_a_per_branch_lift_bound"]
    assert verdict["phi_r_is_the_taylor_jet"]
    assert verdict["local_hensel_already_adaptive"]
    assert verdict["witness_splits_local_from_global"]
    assert verdict["novelty"] == "NONE"
    assert report["first_all_nonsingular"] is None or report["first_all_nonsingular"] > 1
