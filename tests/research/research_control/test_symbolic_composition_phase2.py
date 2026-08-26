"""Live Phase-2 symbolic composition falsifier on frozen v2.3 transitions."""

from __future__ import annotations

from research.research_control.symbolic_composition_phase2 import (
    DOC_PATH,
    JSON_PATH,
    juggler_samples,
    run_phase2,
    write_artifacts,
)
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.symbolic_composition import Phase2Decision, decide_phase2, updated_proposals
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER


def test_juggler_samples_exclude_odd_odd_branch():
    sources = {item.source for item in juggler_samples()}
    assert 3 not in sources
    assert all(item.source % 2 == 1 and item.mid % 2 == 0 for item in juggler_samples())
    assert all(item.image < item.source for item in juggler_samples())


def test_phase2_three_targets_and_artifacts():
    reports = run_phase2(lean_status="PROVED")
    by_name = {item.target: item for item in reports}
    assert set(by_name) == {
        "juggler_sequence",
        "reverse_and_add_base3",
        "home_prime_49",
    }
    assert by_name["juggler_sequence"].classification == "SYMBOLIC_COMPOSITION_PROMISING"
    assert by_name["juggler_sequence"].composition_depth == 2
    assert by_name["juggler_sequence"].lean_status == "PROVED"
    assert by_name["juggler_sequence"].counterexamples == ()
    assert by_name["reverse_and_add_base3"].classification == (
        "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    )
    assert by_name["home_prime_49"].classification == "HOME_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    for report in reports:
        dossier = updated_proposals(report)
        assert [item.rank for item in dossier.proposals] == [1, 2, 3]
        names = [item.attack_name for item in dossier.proposals]
        assert len(set(names)) == 3
        for name in names:
            assert name not in DEFAULT_ATTACK_ORDER
            assert_not_executable(name)
    decision, _reason = decide_phase2(reports)
    assert decision is Phase2Decision.MIXED
    payload = write_artifacts(reports, lean_status="PROVED")
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_2_SYMBOLIC_COMPOSITION_FALSIFIER"
    assert payload["phase2_decision"] == "MIXED"
    assert payload["promoted_concept"] == "odd_even_symbolic_composition"
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MIXED" in text
    assert "odd_even_symbolic_composition" in text
    verify_manifest(load_v2_3_baseline().manifest)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "odd_even_symbolic_composition" not in DEFAULT_ATTACK_ORDER
