"""Phase-9 frontier re-ranking: deterministic selection, no execution."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.frontier_ranking import (
    EXPERIMENT_NAME,
    FORBIDDEN_ATTACKS,
    REQUIRED_CANDIDATE_FIELDS,
    REVERSE_ADD_TARGET,
    AttackProposal,
    AttackProposalDossier,
    FrontierDecision,
    as_proposal_dossier,
    eligible_candidates,
    frozen_candidates,
    frozen_exclusions,
    phase9_payload,
    qualitative_score_milli,
    rank_candidates,
    selected_frontier,
    top3,
)
from research_engine.control.proposals import assert_not_executable
from research_engine.control.types import AttackProposal as ControlProposal
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS, EXPERIMENTAL_ATTACKS


def test_exactly_three_deterministic_top_pairs():
    first = top3()
    second = top3()
    assert [(item.target_id, item.attack_name) for item in first] == [
        (item.target_id, item.attack_name) for item in second
    ]
    assert first[0].target_id == "juggler_sequence"
    assert first[0].attack_name == "odd_odd_branch_composition"
    assert first[1].target_id == "mx_plus_r_7x1_class_obstruction"
    assert first[1].attack_name == "basin_preimage_grammar"
    assert first[2].target_id == "matthews_prize_mod3_avoider"
    assert first[2].attack_name == "basin_preimage_grammar"
    winner = selected_frontier()
    assert winner.pair_id == first[0].pair_id
    assert winner.expected_loot.value == "GREEN"


def test_reverse_add_is_excluded_from_pool_and_selection():
    assert REVERSE_ADD_TARGET not in {item.target_id for item in eligible_candidates()}
    assert any(item["target_id"] == REVERSE_ADD_TARGET for item in frozen_exclusions())
    assert selected_frontier().target_id != REVERSE_ADD_TARGET
    payload = phase9_payload()
    assert payload["reverse_add_reopened"] is False
    assert all(item["target_id"] != REVERSE_ADD_TARGET for item in payload["ranked_candidates"])
    assert all(item["target_id"] != REVERSE_ADD_TARGET for item in payload["candidate_pool"])


def test_machinery_gravity_and_exhausted_juggler_lemma_are_not_ranked():
    names = {item.attack_name for item in eligible_candidates()}
    assert not (names & FORBIDDEN_ATTACKS)
    pairs = {(item.target_id, item.attack_name) for item in rank_candidates()}
    assert ("juggler_sequence", "odd_even_two_step_decrease") not in pairs
    assert ("home_prime_49", "concat_word_composition") not in pairs


def test_required_schema_and_proposal_dossier_roundtrip():
    payload = phase9_payload()
    for field in (
        "candidate_pool",
        "excluded_targets",
        "scoring_basis",
        "ranked_candidates",
        "selected_frontier",
        "supporting_evidence",
        "cheapest_falsifier",
        "decision",
    ):
        assert payload[field]
    assert payload["decision"] == FrontierDecision.SELECTED_FRONTIER.value
    assert payload["experimental_status"] == "PHASE_9_FRONTIER_RERANKING"
    assert payload["engine_control_version"] == "0.2.7"
    assert payload["source_engine"] == "v2.3"
    assert payload["executed"] is False
    for item in frozen_candidates():
        data = item.as_dict()
        for field in REQUIRED_CANDIDATE_FIELDS:
            assert data[field]
    dossier = as_proposal_dossier()
    assert isinstance(dossier, AttackProposalDossier)
    assert len(dossier.proposals) == 3
    rebuilt = AttackProposalDossier.from_dict(dossier.as_dict())
    assert [item.attack_name for item in rebuilt.proposals] == [item.attack_name for item in dossier.proposals]
    for proposal in rebuilt.proposals:
        assert_not_executable(proposal.attack_name)
        assert isinstance(ControlProposal.from_dict(proposal.as_dict()), ControlProposal)
        assert proposal.attack_name not in DEFAULT_ATTACK_ORDER
        assert proposal.attack_name not in EXPERIMENTAL_ATTACKS


def test_score_is_a_prioritization_aid_not_a_probability():
    winner = selected_frontier()
    score = qualitative_score_milli(
        expected_loot=winner.expected_loot,
        frontier_strength=winner.frontier_strength,
        lean_path=winner.lean_path,
        implementation_scope=winner.implementation_scope,
        novelty_risk=winner.novelty_risk,
    )
    assert score == winner.score_milli
    assert score > rank_candidates()[1].score_milli
    assert phase9_payload()["scoring_basis"]["not_calibrated"] is True


def test_engine_module_does_not_import_bt_or_register_attacks():
    from pathlib import Path

    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "control", "frontier_ranking.py"
    ).read_text(encoding="utf-8")
    assert "from bt" not in text
    assert "import bt" not in text
    assert "research.residuals" not in text
    assert EXPERIMENT_NAME not in DEFAULT_ATTACK_ORDER
    assert "odd_odd_branch_composition" not in DEFAULT_ATTACK_ORDER
    assert "basin_preimage_grammar" not in DEFAULT_ATTACK_ORDER
    assert EXPERIMENT_NAME not in EXPERIMENTAL_ATTACKS
    assert "odd_odd_branch_composition" not in EXPERIMENTAL_ATTACKS


def test_frozen_v23_and_flood_order_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert DEFERRED_ATTACKS == ("symbolic",)
    assert baseline.board.by_name()[REVERSE_ADD_TARGET].already_run is True
    assert "phase9_frontier_ranking" not in DEFAULT_ATTACK_ORDER
    assert AttackProposal  # imported for schema compatibility
