"""Live Phase-0 ranking falsifier on frozen v2.3 campaign transitions."""

from __future__ import annotations

from research.research_control.ranking_phase0 import DOC_PATH, JSON_PATH, run_phase0, write_artifacts
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.ranking import Phase0Decision, RankingVerdict, decide_phase0, updated_proposals
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER


def test_phase0_four_targets_proposals_and_artifacts():
    reports = run_phase0()
    by_name = {item.target: item for item in reports}
    assert set(by_name) == {
        "juggler_sequence",
        "reverse_and_add_base3",
        "home_prime_49",
        "cyclic_tag_bit",
    }
    assert by_name["juggler_sequence"].classification is RankingVerdict.RANKING_NEEDS_RICHER_STATE
    assert by_name["reverse_and_add_base3"].classification is RankingVerdict.RANKING_NEEDS_RICHER_STATE
    assert by_name["home_prime_49"].classification is RankingVerdict.RANKING_NEEDS_RICHER_STATE
    assert by_name["cyclic_tag_bit"].classification is RankingVerdict.RANKING_IMPLAUSIBLE
    assert by_name["cyclic_tag_bit"].survivors == ()
    for report in reports:
        assert report.candidate_count == 145
        assert report.transitions_tested >= 3
        assert report.formalization_ready == "not_yet_formalization_ready"
        assert "exact integer" in report.exactness
        dossier = updated_proposals(report)
        assert [item.rank for item in dossier.proposals] == [1, 2, 3]
        names = [item.attack_name for item in dossier.proposals]
        assert len(set(names)) == 3
        for name in names:
            assert name not in DEFAULT_ATTACK_ORDER
            assert_not_executable(name)
    assert updated_proposals(by_name["juggler_sequence"]).proposals[0].attack_name == "odd_even_composed_ranking"
    assert (
        updated_proposals(by_name["reverse_and_add_base3"]).proposals[0].attack_name
        == "reverse_gap_or_palindrome_ranking"
    )
    assert (
        updated_proposals(by_name["home_prime_49"]).proposals[0].attack_name
        == "composite_concat_piecewise_ranking"
    )
    assert (
        updated_proposals(by_name["cyclic_tag_bit"]).proposals[0].attack_name
        == "symbolic_nonlinear_composition"
    )
    decision, _reason = decide_phase0(reports)
    assert decision is Phase0Decision.REFINE
    payload = write_artifacts(reports)
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_0_FALSIFIER"
    assert payload["attack_family"] == "ranking_function_synthesis"
    assert payload["decision"] == "REFINE"
    assert payload["formalization_ready"] == "not_yet_formalization_ready"
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    assert "REFINE" in DOC_PATH.read_text(encoding="utf-8")
    verify_manifest(load_v2_3_baseline().manifest)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "ranking_function_synthesis" not in DEFAULT_ATTACK_ORDER
