"""Non-executable Top-3 attack proposals."""

from __future__ import annotations

import pytest

from research_engine.attacks.result import AttackContext
from research_engine.control.archive import archive_with_control
from research_engine.control.proposals import (
    REGISTERED_ATTACKS,
    assert_not_executable,
    evidence_from_experiment,
    is_registered_attack,
    propose_attacks,
)
from research_engine.control.types import (
    FORBIDDEN_PROPOSAL_NAMES,
    ControlSchemaError,
    ProposalEvidence,
    V2_3_CAMPAIGN_ORDER,
)
from research_engine.memory.store import ResearchMemory
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, run_named_attack
from tests.research_engine.core.test_planner import CountdownSpec

REQUIRED_FIELDS = (
    "rank",
    "attack_name",
    "trigger",
    "mathematical_target",
    "mechanism",
    "required_capability",
    "expected_yield",
    "falsifier",
    "novelty_risk",
    "implementation_scope",
    "confidence",
)


def test_nine_campaigns_serialize_exactly_three_unique_ranks():
    memory = ResearchMemory.load_historical()
    for name in V2_3_CAMPAIGN_ORDER:
        experiment = memory.get(name)
        dossier = propose_attacks(evidence_from_experiment(experiment), campaign_id=name)
        ranks = [item.rank for item in dossier.proposals]
        names = [item.attack_name for item in dossier.proposals]
        assert ranks == [1, 2, 3]
        assert len(set(names)) == 3
        for proposal in dossier.proposals:
            payload = proposal.as_dict()
            for field in REQUIRED_FIELDS:
                assert payload[field]
            assert proposal.attack_name not in REGISTERED_ATTACKS
            assert proposal.attack_name not in DEFAULT_ATTACK_ORDER
            assert proposal.attack_name.lower() not in FORBIDDEN_PROPOSAL_NAMES
            assert_not_executable(proposal.attack_name)


def test_proposals_are_not_executable_through_the_registry():
    spec = CountdownSpec()
    context = AttackContext()
    for name in (
        "ranking_function_synthesis",
        "basin_preimage_grammar",
        "global_vanishing_congruence",
    ):
        assert is_registered_attack(name) is False
        with pytest.raises(KeyError):
            run_named_attack(name, spec, context)


def test_generic_proposal_names_rejected():
    with pytest.raises(ControlSchemaError):
        assert_not_executable("more search")


def test_thin_evidence_still_emits_three_low_confidence():
    evidence = ProposalEvidence(experiment_id="thin", target="thin")
    dossier = propose_attacks(evidence, campaign_id="thin")
    assert len(dossier.proposals) == 3
    assert {item.rank for item in dossier.proposals} == {1, 2, 3}
    assert all(item.confidence.value == "LOW" for item in dossier.proposals)


def test_archive_attaches_proposals_without_mutating_experiment():
    memory = ResearchMemory.load_historical()
    experiment = memory.get("mx_plus_r_7x1_class_obstruction")
    before = experiment.as_dict()
    record = archive_with_control(experiment)
    assert experiment.as_dict() == before
    assert record.close_tag.value == "CLOSE_FALSE_OBSTRUCTION"
    assert record.mathematical_status.value == "STRONG_NEGATIVE"
    assert len(record.proposals.proposals) == 3
    assert "close_tag" not in before
