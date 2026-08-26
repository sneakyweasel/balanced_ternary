"""Live Phase-12 Juggler parity-drift falsifier."""

from __future__ import annotations

import json

from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.research_control.juggler_macro_phase11 import JSON_PATH as PHASE11_JSON
from research.research_control.juggler_odd_odd_phase10 import (
    JSON_PATH as PHASE10_JSON,
    frozen_seeds,
)
from research.research_control.juggler_parity_drift_phase12 import (
    DOC_PATH,
    JSON_PATH,
    LEAN_PATH,
    frozen_drift_samples,
    run_phase12,
    write_artifacts,
)
from research.research_control.phase9_frontier_ranking import JSON_PATH as PHASE9_JSON
from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_involution_phase8 import JSON_PATH as PHASE8_JSON
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.juggler_parity_drift import (
    EXPERIMENT_NAME,
    MAX_DEPTH,
    DriftClass,
    ranked_candidates,
)
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_phase12_three_candidates_and_artifacts():
    payload = write_artifacts()
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION == "0.2.7"
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_12_JUGGLER_PARITY_DRIFT_FALSIFIER"
    assert payload["target"] == "juggler_sequence"
    assert payload["max_composition_depth"] == MAX_DEPTH == 5
    assert payload["experiment_name"] == EXPERIMENT_NAME
    by_name = {item["name"]: item for item in payload["candidates"]}
    assert [item["rank"] for item in payload["candidates"]] == [1, 2, 3]
    assert len(ranked_candidates()) == 3
    one = by_name["one_step_increment_bounds"]
    block = by_name["oooee_conditional_contraction"]
    shortest = by_name["shortest_negative_block"]
    assert one["survived"] is True
    assert one["loot_eligible"] is False
    assert block["survived"] is True
    assert block["parity_word"] == "OOOEE"
    assert shortest["survived"] is True
    assert shortest["parity_word"] == "EE"
    assert payload["decision"] == DriftClass.PARITY_DRIFT_GREEN_LOOT.value
    assert payload["loot_status"] == "PARITY_DRIFT_GREEN_LOOT"
    assert payload["lean_status"] == "PROVED"
    assert payload["anti_overclaim"]["global_termination"] is False
    assert payload["anti_overclaim"]["parity_frequency_theorem"] is False
    assert payload["global_consequence"] == "LOCAL_BRANCH_LAW"
    names = [item["attack_name"] for item in payload["top3_update"]["proposals"]]
    assert names[0] == "parity_drift_block"
    assert "parity_drift_block" not in DEFAULT_ATTACK_ORDER
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "PARITY_DRIFT_GREEN_LOOT" in text
    assert "LOCAL_BRANCH_LAW" in text
    assert "Level C" in text


def test_phase12_does_not_expand_census_or_depth():
    allowed = set(JUGGLER_WINDOW) | {int(item) for item in juggler_orbit(13)["path"]}
    assert set(frozen_seeds()) <= allowed
    samples = frozen_drift_samples()
    assert {item.source for item in samples} <= allowed
    assert all(item.depth <= 5 for item in samples)
    assert any(item.word == "OOOEE" and item.source == 3 and item.image == 2 for item in samples)
    assert any(item.word == "EE" and item.source == 4 for item in samples)
    assert MAX_DEPTH == 5


def test_existing_juggler_lemmas_unchanged_and_oooee_present():
    text = LEAN_PATH.read_text(encoding="utf-8")
    assert "theorem floorPower_odd_even_two_step_lt" in text
    assert "exact sqrt_sqrt_n_cubed_lt hn" in text
    assert "theorem floorPower_odd_odd_two_step_gt" in text
    assert "theorem floorPower_odd_macro_direction" in text
    assert "theorem floorPower_oooee_five_step_lt" in text
    assert "sorry" not in text
    assert "admit" not in text


def test_phase12_does_not_thaw_or_rewrite_history():
    assert "juggler_parity_drift_phase12" not in DEFAULT_ATTACK_ORDER
    assert "parity_drift_block" not in DEFAULT_ATTACK_ORDER
    assert "juggler_parity_drift_phase12" not in EXPERIMENTAL_ATTACKS
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    phase8 = json.loads(PHASE8_JSON.read_text(encoding="utf-8"))
    phase9 = json.loads(PHASE9_JSON.read_text(encoding="utf-8"))
    phase10 = json.loads(PHASE10_JSON.read_text(encoding="utf-8"))
    phase11 = json.loads(PHASE11_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase8["decision"] == "REVERSE_INVOLUTION_REFUTED"
    assert phase9["decision"] == "SELECTED_FRONTIER"
    assert phase10["decision"] == "JUGGLER_ODD_ODD_GREEN_LOOT"
    assert phase11["decision"] == "MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE"
    run_phase12()
    assert json.loads(PHASE11_JSON.read_text(encoding="utf-8"))["decision"] == "MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE"
    assert json.loads(PHASE10_JSON.read_text(encoding="utf-8"))["decision"] == "JUGGLER_ODD_ODD_GREEN_LOOT"
    assert json.loads(PHASE3_JSON.read_text(encoding="utf-8"))["attack_name"] == "odd_even_two_step_decrease"
