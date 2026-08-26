"""Live Phase-11 Juggler macro-grammar falsifier."""

from __future__ import annotations

import json

from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.research_control.juggler_macro_phase11 import (
    DOC_PATH,
    JSON_PATH,
    LEAN_PATH,
    frozen_odd_macro_samples,
    run_phase11,
    write_artifacts,
)
from research.research_control.juggler_odd_odd_phase10 import (
    JSON_PATH as PHASE10_JSON,
    frozen_seeds,
)
from research.research_control.phase9_frontier_ranking import JSON_PATH as PHASE9_JSON
from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_involution_phase8 import JSON_PATH as PHASE8_JSON
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.juggler_macro import DEPTH, EXPERIMENT_NAME, MacroClass, ranked_candidates
from research_engine.control.juggler_odd_odd import in_d_oe, in_d_oo
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_phase11_three_candidates_and_artifacts():
    payload = write_artifacts()
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION == "0.2.7"
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_11_JUGGLER_MACRO_GRAMMAR_FALSIFIER"
    assert payload["target"] == "juggler_sequence"
    assert payload["composition_depth"] == DEPTH == 2
    assert payload["experiment_name"] == EXPERIMENT_NAME
    by_name = {item["name"]: item for item in payload["candidates"]}
    assert [item["rank"] for item in payload["candidates"]] == [1, 2, 3]
    assert len(ranked_candidates()) == 3
    combined = by_name["combined_direction_law"]
    parity = by_name["branch_determines_t2_parity"]
    survival = by_name["contraction_exits_odd_macro"]
    assert combined["survived"] is True
    assert parity["survived"] is False
    assert parity["counterexample"]["source"] == 5
    assert parity["failure_class"] == "MACRO_PARITY_NOT_DETERMINISTIC"
    assert survival["survived"] is False
    assert survival["counterexample"]["source"] == 15
    assert survival["failure_class"] == "DIRECTION_SURVIVAL_DECOUPLING"
    assert payload["decision"] == MacroClass.MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE.value
    assert payload["loot_status"] == "NO_NEW_LOOT"
    assert payload["lean_status"] == "COMPOSITION_OF_KNOWN_FACTS"
    assert payload["macro_state"]["status"] == "MACRO_STATE_INSUFFICIENT"
    assert payload["anti_overclaim"]["global_termination"] is False
    assert payload["anti_overclaim"]["combined_is_new_loot"] is False
    assert payload["global_consequence"] == "LOCAL_BRANCH_LAW"
    names = [item["attack_name"] for item in payload["top3_update"]["proposals"]]
    assert names[0] == "basin_preimage_grammar"
    assert names[1] == "odd_odd_symbolic_composition"
    assert "juggler_macro_grammar" not in names
    assert "macro_state_needs_richer_information" in payload["top3_update"]["notes"]
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE" in text
    assert "COMPOSITION_OF_KNOWN_FACTS" in text
    assert "NO_NEW_LOOT" in text


def test_phase11_does_not_expand_census_or_depth():
    allowed = set(JUGGLER_WINDOW) | {int(item) for item in juggler_orbit(13)["path"]}
    assert set(frozen_seeds()) <= allowed
    samples = frozen_odd_macro_samples()
    assert {item.source for item in samples} <= allowed
    assert any(item.source == 1 and item.image == 1 for item in samples)
    assert any(item.source == 5 and item.image == 36 for item in samples)
    assert any(item.source == 15 and item.image == 7 for item in samples)
    odds_ge3 = [item for item in samples if item.source >= 3]
    assert all(item.source % 2 == 1 for item in odds_ge3)
    oe = {item.source for item in odds_ge3 if item.branch == "E"}
    oo = {item.source for item in odds_ge3 if item.branch == "O"}
    assert not (oe & oo)
    assert oe | oo == {item.source for item in odds_ge3}
    assert all(in_d_oe(n) for n in oe)
    assert all(in_d_oo(n) for n in oo)
    assert DEPTH == 2
    assert samples[0].as_dict()["composition_depth"] == 2


def test_existing_juggler_lemmas_unchanged_and_combined_present():
    text = LEAN_PATH.read_text(encoding="utf-8")
    assert "theorem floorPower_odd_even_two_step_lt" in text
    assert "exact sqrt_sqrt_n_cubed_lt hn" in text
    assert "theorem floorPower_odd_odd_two_step_gt" in text
    assert "theorem floorPower_odd_macro_direction" in text
    assert "sorry" not in text
    assert "admit" not in text


def test_phase11_does_not_thaw_or_rewrite_history():
    assert "juggler_macro_phase11" not in DEFAULT_ATTACK_ORDER
    assert "juggler_macro_grammar" not in DEFAULT_ATTACK_ORDER
    assert "odd_odd_symbolic_composition" not in DEFAULT_ATTACK_ORDER
    assert "juggler_macro_phase11" not in EXPERIMENTAL_ATTACKS
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    phase8 = json.loads(PHASE8_JSON.read_text(encoding="utf-8"))
    phase9 = json.loads(PHASE9_JSON.read_text(encoding="utf-8"))
    phase10 = json.loads(PHASE10_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase8["decision"] == "REVERSE_INVOLUTION_REFUTED"
    assert phase9["decision"] == "SELECTED_FRONTIER"
    assert phase10["decision"] == "JUGGLER_ODD_ODD_GREEN_LOOT"
    run_phase11()
    assert json.loads(PHASE10_JSON.read_text(encoding="utf-8"))["decision"] == "JUGGLER_ODD_ODD_GREEN_LOOT"
    assert json.loads(PHASE3_JSON.read_text(encoding="utf-8"))["attack_name"] == "odd_even_two_step_decrease"
    assert json.loads(PHASE9_JSON.read_text(encoding="utf-8"))["decision"] == "SELECTED_FRONTIER"
