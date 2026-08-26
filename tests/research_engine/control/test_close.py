"""CLOSE taxonomy and mathematical-status independence."""

from __future__ import annotations

import pytest

from research_engine.control.close import (
    parse_close_tag,
    refuse_resolved_from_finite,
    validate_pair,
    validate_record,
)
from research_engine.control.migrate import V2_3_INFERENCE, infer_classification
from research_engine.control.proposals import propose_attacks, evidence_from_experiment
from research_engine.control.types import (
    AttackProposal,
    AttackProposalDossier,
    CampaignControlRecord,
    CloseTag,
    Confidence,
    ControlSchemaError,
    ExecutionStatus,
    ImplementationScope,
    MathematicalStatus,
    NoveltyRisk,
    V2_3_CAMPAIGN_ORDER,
)
from research_engine.memory.store import ResearchMemory


def _stub_proposals() -> AttackProposalDossier:
    def one(rank: int, name: str) -> AttackProposal:
        return AttackProposal(
            rank=rank,
            attack_name=name,
            trigger="t",
            mathematical_target="m",
            mechanism="k",
            required_capability="c",
            expected_yield="exact lemma",
            falsifier="f",
            novelty_risk=NoveltyRisk.LOW,
            implementation_scope=ImplementationScope.SMALL,
            confidence=Confidence.LOW,
        )

    return AttackProposalDossier(
        proposals=(
            one(1, "ranking_function_synthesis"),
            one(2, "basin_preimage_grammar"),
            one(3, "residue_valuation_coupling"),
        )
    )


def test_invalid_close_tag_rejected():
    with pytest.raises(ControlSchemaError):
        parse_close_tag("CLOSE_HARDER")


def test_close_skip_boundary_plus_frontier_is_valid():
    validate_pair(
        ExecutionStatus.CLOSE,
        MathematicalStatus.FRONTIER,
        CloseTag.CLOSE_SKIP_BOUNDARY,
    )


def test_close_false_obstruction_plus_strong_negative_is_valid():
    validate_pair(
        ExecutionStatus.CLOSE,
        MathematicalStatus.STRONG_NEGATIVE,
        CloseTag.CLOSE_FALSE_OBSTRUCTION,
    )


def test_finite_census_cannot_be_resolved():
    with pytest.raises(ControlSchemaError):
        validate_pair(
            ExecutionStatus.CLOSE,
            MathematicalStatus.RESOLVED,
            CloseTag.CLOSE_FINITE_CENSUS,
        )
    assert refuse_resolved_from_finite("FINITE_CENSUS prefix horizon 16") is MathematicalStatus.UNRESOLVED


def test_close_does_not_imply_resolved():
    record = CampaignControlRecord(
        campaign_id="x",
        experiment_id="x",
        target="x",
        execution_status=ExecutionStatus.CLOSE,
        mathematical_status=MathematicalStatus.FRONTIER,
        proposals=_stub_proposals(),
        close_tag=CloseTag.CLOSE_SKIP_BOUNDARY,
    )
    validate_record(record)
    assert record.execution_status is ExecutionStatus.CLOSE
    assert record.mathematical_status is not MathematicalStatus.RESOLVED


def test_exactly_one_primary_close_tag_required():
    with pytest.raises(ControlSchemaError):
        validate_pair(ExecutionStatus.CLOSE, MathematicalStatus.UNRESOLVED, None)


def test_v2_3_inference_table_matches_the_nine():
    memory = ResearchMemory.load_historical()
    for name in V2_3_CAMPAIGN_ORDER:
        tag, status, reason = V2_3_INFERENCE[name]
        experiment = memory.get(name)
        inferred_tag, inferred_status, provenance, _ = infer_classification(experiment)
        assert inferred_tag is tag
        assert inferred_status is status
        assert provenance.value == "INFERRED"
        assert inferred_status is not MathematicalStatus.RESOLVED
        dossier = propose_attacks(evidence_from_experiment(experiment), campaign_id=name)
        assert len(dossier.proposals) == 3
