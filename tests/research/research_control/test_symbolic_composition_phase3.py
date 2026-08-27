"""Live Phase-3 restricted symbolic-composition attack on frozen campaign maps."""

from __future__ import annotations

import json

from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import (
    DOC_PATH,
    JSON_PATH,
    REPO_ROOT,
    decide_phase3,
    run_phase3,
    write_artifacts,
)
from research_engine.attacks.restricted_symbolic_composition import (
    ENABLE_RESTRICTED_SYMBOLIC_COMPOSITION,
    FAMILY_NAME,
    RULE_NAME,
)
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS, EXPERIMENTAL_ATTACKS


def test_phase3_juggler_and_negative_controls():
    reports = run_phase3()
    by_name = {item.target_id: item for item in reports}
    assert set(by_name) >= {
        "juggler_sequence",
        "reverse_and_add_base3",
        "home_prime_49",
        "cyclic_tag_bit",
    }
    juggler = by_name["juggler_sequence"]
    assert juggler.applicability == "APPLICABLE"
    assert juggler.candidate == "T^2(x) < x"
    assert juggler.lean_status == "PROVED"
    assert juggler.lean_theorem.endswith("floorPower_odd_even_two_step_lt")
    assert juggler.mathematical_status == "NEW_STRUCTURAL_LEMMA"
    assert juggler.global_consequence == "NONE"
    assert juggler.depth == 2
    from research.juggler_sequence.lean_paths import juggler_text

    lean = juggler_text()
    assert "theorem floorPower_odd_even_two_step_lt" in lean
    assert "sorry" not in lean
    assert "admit" not in lean
    assert by_name["reverse_and_add_base3"].applicability == "NOT_APPLICABLE"
    assert by_name["home_prime_49"].applicability == "NOT_APPLICABLE"
    assert by_name["cyclic_tag_bit"].applicability == "NOT_APPLICABLE"
    assert by_name["reverse_and_add_base3"].failure_reason == "MAP_MISMATCH"
    assert by_name["home_prime_49"].failure_reason == "MAP_MISMATCH"
    assert by_name["cyclic_tag_bit"].failure_reason == "MAP_MISMATCH"
    decision, _reason = decide_phase3(reports)
    assert decision == "PROMOTE_RESTRICTED"
    payload = write_artifacts(reports)
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["experimental_status"] == "PHASE_3_RESTRICTED_SYMBOLIC_ATTACK"
    assert payload["decision"] == "PROMOTE_RESTRICTED"
    assert payload["attack_name"] == RULE_NAME
    assert payload["gated"] is True
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "PROMOTE_RESTRICTED" in text
    assert "NONE" in text
    assert "TERMINATION_PROVED" not in text


def test_phase3_does_not_thaw_or_rewrite_history():
    assert ENABLE_RESTRICTED_SYMBOLIC_COMPOSITION is False
    assert FAMILY_NAME not in DEFAULT_ATTACK_ORDER
    assert RULE_NAME not in DEFAULT_ATTACK_ORDER
    assert EXPERIMENTAL_ATTACKS.isdisjoint(DEFAULT_ATTACK_ORDER)
    assert DEFERRED_ATTACKS == ("symbolic",)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase2["promoted_concept"] == "odd_even_symbolic_composition"
    assert phase2["experimental_status"] == "PHASE_2_SYMBOLIC_COMPOSITION_FALSIFIER"
