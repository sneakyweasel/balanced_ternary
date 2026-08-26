"""Live Phase-4 reverse-add two-step composition falsifier."""

from __future__ import annotations

import json

from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_composition_phase4 import (
    DOC_PATH,
    JSON_PATH,
    run_phase4,
    write_artifacts,
)
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.reverse_add_composition import ReverseCompositionClass
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_phase4_three_candidates_and_artifacts():
    _samples, outcomes, classification, _reason = run_phase4()
    assert [item.rank for item in outcomes] == [1, 2, 3]
    by_name = {item.name: item for item in outcomes}
    cancel = by_name["reverse_cancellation"]
    sign = by_name["two_step_sign_preservation"]
    length = by_name["two_step_length_plus_one"]
    assert cancel.survived is False
    assert cancel.failure_class == "CANCELLATION_FAILURE"
    assert cancel.counterexample is not None
    assert cancel.counterexample.source == 1
    assert cancel.counterexample.image == 0
    assert sign.survived is False
    assert sign.failure_class == "SIGN_REVERSAL"
    assert sign.counterexample is not None
    assert sign.counterexample.source == 1
    assert length.survived is True
    assert length.counterexample is None
    assert classification is ReverseCompositionClass.REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE
    payload = write_artifacts(_samples)
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_4_REVERSE_ADD_COMPOSITION_FALSIFIER"
    assert payload["decision"] == "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    assert payload["green_loot"] == "NO_NEW_LOOT"
    assert payload["lean_status"] == "NOT_YET_FORMALIZATION_READY"
    assert payload["composition_depth"] == 2
    names = [item["attack_name"] for item in payload["top3_attack_update"]["proposals"]]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "reverse_add_symbolic_composition" not in names
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE" in text
    assert "NO_NEW_LOOT" in text


def test_phase4_does_not_thaw_or_rewrite_history():
    assert "reverse_add_composition_phase4" not in DEFAULT_ATTACK_ORDER
    assert "reverse_add_symbolic_composition" not in DEFAULT_ATTACK_ORDER
    assert "reverse_add_composition_phase4" not in EXPERIMENTAL_ATTACKS
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase3["experimental_status"] == "PHASE_3_RESTRICTED_SYMBOLIC_ATTACK"
