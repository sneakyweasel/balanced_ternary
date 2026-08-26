"""Load frozen evidence and write the Phase-9 frontier ranking artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from research_engine.control.baseline import load_v2_3_baseline
from research_engine.control.frontier_ranking import (
    EXPERIMENT_NAME,
    REVERSE_ADD_TARGET,
    as_proposal_dossier,
    phase9_payload,
    render_phase9_markdown,
    selected_frontier,
    top3,
)
from research_engine.control.proposals import assert_not_executable, evidence_from_experiment, propose_attacks
from research_engine.control.types import V2_3_CAMPAIGN_ORDER
from research_engine.memory.store import BOARD_PATH, SEED_PATH

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "phase9_frontier_ranking.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "phase9_frontier_ranking.md"


def assert_historical_consumption_unchanged() -> None:
    baseline = load_v2_3_baseline()
    board = baseline.board.by_name()
    if not board[REVERSE_ADD_TARGET].already_run:
        raise RuntimeError("Phase-9 must not reset reverse-add consumption")
    for name in V2_3_CAMPAIGN_ORDER:
        if name not in board:
            raise RuntimeError(f"missing frozen board target {name}")
        if not board[name].already_run:
            raise RuntimeError(f"Phase-9 must not reset already_run for {name}")
    if SEED_PATH.resolve() == JSON_PATH.resolve() or BOARD_PATH.resolve() == JSON_PATH.resolve():
        raise RuntimeError("Phase-9 artifacts must not overwrite historical seed files")


def live_top3_names(target_id: str) -> tuple[str, ...]:
    baseline = load_v2_3_baseline()
    experiment = baseline.memory.get(target_id)
    dossier = propose_attacks(evidence_from_experiment(experiment), campaign_id=target_id)
    return tuple(item.attack_name for item in dossier.proposals)


def run_phase9() -> dict:
    assert_historical_consumption_unchanged()
    chosen = top3()
    winner = selected_frontier()
    dossier = as_proposal_dossier()
    for proposal in dossier.proposals:
        assert_not_executable(proposal.attack_name)
    if winner.pair_id != chosen[0].pair_id:
        raise RuntimeError("selected frontier is not rank 1")
    if winner.target_id == REVERSE_ADD_TARGET:
        raise RuntimeError("reverse-add must not win Phase-9")
    payload = phase9_payload()
    mx_names = live_top3_names("mx_plus_r_7x1_class_obstruction")
    matthews_names = live_top3_names("matthews_prize_mod3_avoider")
    if "basin_preimage_grammar" not in mx_names:
        raise RuntimeError("mx_plus_r live Top-3 no longer contains basin_preimage_grammar")
    if "basin_preimage_grammar" not in matthews_names:
        raise RuntimeError("matthews live Top-3 no longer contains basin_preimage_grammar")
    payload["supporting_evidence"]["live_top3_check"] = {
        "mx_plus_r_7x1_class_obstruction": list(mx_names),
        "matthews_prize_mod3_avoider": list(matthews_names),
        "odd_odd_source": "symbolic_composition_phase2 updated_proposals",
    }
    return payload


def write_artifacts(payload: dict | None = None) -> dict:
    data = payload if payload is not None else run_phase9()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase9_markdown(data), encoding="utf-8")
    assert_historical_consumption_unchanged()
    return data
