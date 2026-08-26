"""Live Phase-1 enriched ranking falsifier on frozen v2.3 transitions."""

from __future__ import annotations

from research.research_control.ranking_phase1 import (
    DOC_PATH,
    JSON_PATH,
    reverse_gap,
    run_phase1,
    write_artifacts,
)
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.ranking_phase1 import Phase1Decision, decide_phase1, updated_proposals
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER


def test_reverse_gap_is_canonical_l1_and_handles_zero():
    assert reverse_gap(0) == 0
    assert reverse_gap(1) == 0
    assert reverse_gap(-1) == 0
    assert reverse_gap(2) == 4
    assert reverse_gap(-2) == reverse_gap(2)


def test_phase1_three_targets_and_artifacts():
    reports = run_phase1()
    by_name = {item.target: item for item in reports}
    assert set(by_name) == {
        "juggler_sequence",
        "reverse_and_add_base3",
        "home_prime_49",
    }
    assert by_name["juggler_sequence"].classification == "COMPOSED_RANKING_PROMISING"
    assert by_name["juggler_sequence"].transition_depth == 2
    assert by_name["juggler_sequence"].survivors
    assert by_name["reverse_and_add_base3"].classification == "REVERSE_GAP_IMPLAUSIBLE"
    assert by_name["reverse_and_add_base3"].survivors == ()
    assert by_name["home_prime_49"].classification == "PIECEWISE_RANKING_NEEDS_RICHER_STATE"
    assert by_name["home_prime_49"].survivors == ()
    for report in reports:
        dossier = updated_proposals(report)
        assert [item.rank for item in dossier.proposals] == [1, 2, 3]
        names = [item.attack_name for item in dossier.proposals]
        assert len(set(names)) == 3
        for name in names:
            assert name not in DEFAULT_ATTACK_ORDER
            assert_not_executable(name)
    decision, _reason = decide_phase1(reports)
    assert decision is Phase1Decision.MIXED
    payload = write_artifacts(reports)
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_1_ENRICHED_RANKING_FALSIFIER"
    assert payload["ranking_phase1_decision"] == "MIXED"
    assert payload["formalization_ready"] == "not_yet_formalization_ready"
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    assert "MIXED" in DOC_PATH.read_text(encoding="utf-8")
    verify_manifest(load_v2_3_baseline().manifest)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "odd_even_composed_ranking" not in DEFAULT_ATTACK_ORDER
