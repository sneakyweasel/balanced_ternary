"""Live Phase-9 frontier ranking artifacts. Selection only."""

from __future__ import annotations

import json

from research.research_control.phase9_frontier_ranking import (
    DOC_PATH,
    JSON_PATH,
    assert_historical_consumption_unchanged,
    live_top3_names,
    run_phase9,
    write_artifacts,
)
from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_involution_phase8 import JSON_PATH as PHASE8_JSON
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.frontier_ranking import REVERSE_ADD_TARGET, REQUIRED_CANDIDATE_FIELDS
from research_engine.control.proposals import assert_not_executable
from research_engine.control.types import ENGINE_CONTROL_VERSION, AttackProposalDossier
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_phase9_writes_selected_frontier_without_execution():
    assert_historical_consumption_unchanged()
    payload = write_artifacts()
    assert payload["decision"] == "SELECTED_FRONTIER"
    assert payload["executed"] is False
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_9_FRONTIER_RERANKING"
    selected = payload["selected_frontier"]
    assert selected["target_id"] == "juggler_sequence"
    assert selected["attack_name"] == "odd_odd_branch_composition"
    assert selected["expected_loot"] == "GREEN"
    assert payload["backup_frontier_1"]["target_id"] == "mx_plus_r_7x1_class_obstruction"
    assert payload["backup_frontier_2"]["target_id"] == "matthews_prize_mod3_avoider"
    assert payload["reverse_add_reopened"] is False
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "SELECTED_FRONTIER" in text
    assert "reverse-and-add" in text.lower() or "reverse-add" in text.lower()
    dossier = AttackProposalDossier.from_dict(payload["top3_attack_update"])
    assert len(dossier.proposals) == 3
    for proposal in dossier.proposals:
        assert_not_executable(proposal.attack_name)
    for item in payload["ranked_candidates"][:3]:
        for field in REQUIRED_CANDIDATE_FIELDS:
            assert item[field]


def test_phase9_live_dossiers_support_basin_backups():
    assert "basin_preimage_grammar" in live_top3_names("mx_plus_r_7x1_class_obstruction")
    assert "basin_preimage_grammar" in live_top3_names("matthews_prize_mod3_avoider")
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    juggler_names = [
        item["attack_name"]
        for item in phase2["updated_proposals"]["juggler_sequence"]["proposals"]
    ]
    assert "odd_odd_branch_composition" in juggler_names


def test_phase9_does_not_thaw_or_rewrite_history():
    assert EXPERIMENTAL_ATTACKS == frozenset(
        {"restricted_symbolic_composition", "odd_even_two_step_decrease"}
    )
    assert "phase9_frontier_ranking" not in DEFAULT_ATTACK_ORDER
    assert "odd_odd_branch_composition" not in DEFAULT_ATTACK_ORDER
    assert "basin_preimage_grammar" not in DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    board = load_v2_3_baseline().board.by_name()
    assert board[REVERSE_ADD_TARGET].already_run is True
    assert SEED_PATH.is_file()
    assert BOARD_PATH.is_file()
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    phase8 = json.loads(PHASE8_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase8["decision"] == "REVERSE_INVOLUTION_REFUTED"
    run_phase9()
    assert_historical_consumption_unchanged()
    assert json.loads(PHASE8_JSON.read_text(encoding="utf-8"))["decision"] == "REVERSE_INVOLUTION_REFUTED"
