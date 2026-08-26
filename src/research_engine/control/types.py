"""v2.4 research-control types. Not attacks and not a theorem ledger."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

ENGINE_CONTROL_VERSION = "0.2.7"
BASELINE_IDENTIFIER = "RESEARCH_ENGINE_V2_3_BASELINE"
EXECUTION_ENGINE = "v2.4_control_v2.3"

V2_3_CAMPAIGN_ORDER: tuple[str, ...] = (
    "mx_plus_r_7x1_class_obstruction",
    "weak_collatz_floor_5x4_rplus",
    "matthews_prize_mod3_avoider",
    "companion_shift_order6_zero_class",
    "skolem_order5_unconditional",
    "juggler_sequence",
    "reverse_and_add_base3",
    "home_prime_49",
    "cyclic_tag_bit",
)

REPLAY_V22_TARGETS: tuple[str, ...] = (
    "skolem_order2_known_zero",
    "switching_affine_z2_origin",
)

FORBIDDEN_PROPOSAL_NAMES: frozenset[str] = frozenset(
    {
        "more search",
        "bigger census",
        "try harder",
        "more_search",
        "bigger_census",
        "try_harder",
    }
)


class CloseTag(str, Enum):
    """Primary close tag. Exactly one on a CLOSE campaign."""

    CLOSE_KNOWN = "CLOSE_KNOWN"
    CLOSE_REPARAMETERIZATION = "CLOSE_REPARAMETERIZATION"
    CLOSE_FALSE_OBSTRUCTION = "CLOSE_FALSE_OBSTRUCTION"
    CLOSE_FINITE_CENSUS = "CLOSE_FINITE_CENSUS"
    CLOSE_SKIP_BOUNDARY = "CLOSE_SKIP_BOUNDARY"
    CLOSE_SPEC_MISMATCH = "CLOSE_SPEC_MISMATCH"
    CLOSE_NO_PROMOTION = "CLOSE_NO_PROMOTION"


class ExecutionStatus(str, Enum):
    """Laboratory branch decision of the campaign. Independent of math status."""

    CLOSE = "CLOSE"
    PARK = "PARK"
    PROMOTE = "PROMOTE"


class MathematicalStatus(str, Enum):
    """Status of the investigated mathematical question. Not implied by CLOSE."""

    RESOLVED = "RESOLVED"
    STRONG_NEGATIVE = "STRONG_NEGATIVE"
    FRONTIER = "FRONTIER"
    UNRESOLVED = "UNRESOLVED"


class FieldProvenance(str, Enum):
    EXPLICIT = "EXPLICIT"
    MIGRATED = "MIGRATED"
    INFERRED = "INFERRED"


class CampaignType(str, Enum):
    LIVE = "LIVE"
    REPLAY = "REPLAY"
    HISTORICAL_V23 = "HISTORICAL_V23"


class NoveltyRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ImplementationScope(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class Confidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ReplayObservationClass(str, Enum):
    HISTORICAL_REPRODUCTION = "HISTORICAL_REPRODUCTION"
    HISTORICAL_REFINEMENT = "HISTORICAL_REFINEMENT"
    NEW_FORMULATION = "NEW_FORMULATION"
    NEW_FALSIFICATION = "NEW_FALSIFICATION"
    NEW_CONJECTURE = "NEW_CONJECTURE"
    NEW_STRUCTURAL_LEMMA = "NEW_STRUCTURAL_LEMMA"
    NEW_THEOREM = "NEW_THEOREM"


STRONG_MATHEMATICAL_YIELD: frozenset[ReplayObservationClass] = frozenset(
    {
        ReplayObservationClass.NEW_CONJECTURE,
        ReplayObservationClass.NEW_STRUCTURAL_LEMMA,
        ReplayObservationClass.NEW_THEOREM,
    }
)

COMPARISON_DIMENSIONS: tuple[str, ...] = (
    "mapping_recovered",
    "structural_observations",
    "candidate_hypotheses",
    "falsifiers",
    "scout_blind_behavior",
    "mathematical_yield",
    "lean_certification",
    "close_tag",
    "mathematical_status",
)


class ControlSchemaError(ValueError):
    """Invalid control-layer record."""


@dataclass(frozen=True)
class AttackProposal:
    """One non-executable mathematically motivated next attack."""

    rank: int
    attack_name: str
    trigger: str
    mathematical_target: str
    mechanism: str
    required_capability: str
    expected_yield: str
    falsifier: str
    novelty_risk: NoveltyRisk
    implementation_scope: ImplementationScope
    confidence: Confidence
    novelty_risk_reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "attack_name": self.attack_name,
            "trigger": self.trigger,
            "mathematical_target": self.mathematical_target,
            "mechanism": self.mechanism,
            "required_capability": self.required_capability,
            "expected_yield": self.expected_yield,
            "falsifier": self.falsifier,
            "novelty_risk": self.novelty_risk.value,
            "implementation_scope": self.implementation_scope.value,
            "confidence": self.confidence.value,
            "novelty_risk_reason": self.novelty_risk_reason,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> AttackProposal:
        return cls(
            rank=int(data["rank"]),
            attack_name=str(data["attack_name"]),
            trigger=str(data["trigger"]),
            mathematical_target=str(data["mathematical_target"]),
            mechanism=str(data["mechanism"]),
            required_capability=str(data["required_capability"]),
            expected_yield=str(data["expected_yield"]),
            falsifier=str(data["falsifier"]),
            novelty_risk=NoveltyRisk(data["novelty_risk"]),
            implementation_scope=ImplementationScope(data["implementation_scope"]),
            confidence=Confidence(data["confidence"]),
            novelty_risk_reason=str(data.get("novelty_risk_reason") or ""),
        )


@dataclass(frozen=True)
class AttackProposalDossier:
    """Exactly three ranked non-executable proposals."""

    proposals: tuple[AttackProposal, ...]
    campaign_id: str = ""
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "proposals": [item.as_dict() for item in self.proposals],
            "notes": list(self.notes),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> AttackProposalDossier:
        return cls(
            proposals=tuple(AttackProposal.from_dict(item) for item in (data.get("proposals") or ())),
            campaign_id=str(data.get("campaign_id") or ""),
            notes=tuple(str(item) for item in (data.get("notes") or ())),
        )


@dataclass(frozen=True)
class ReplayMetadata:
    campaign_type: CampaignType = CampaignType.REPLAY
    source_engine: str = "v2.2"
    execution_engine: str = EXECUTION_ENGINE
    source_target_id: str = ""
    source_campaign_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "campaign_type": self.campaign_type.value,
            "source_engine": self.source_engine,
            "execution_engine": self.execution_engine,
            "source_target_id": self.source_target_id,
            "source_campaign_id": self.source_campaign_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ReplayMetadata:
        return cls(
            campaign_type=CampaignType(data.get("campaign_type") or CampaignType.REPLAY.value),
            source_engine=str(data.get("source_engine") or "v2.2"),
            execution_engine=str(data.get("execution_engine") or EXECUTION_ENGINE),
            source_target_id=str(data.get("source_target_id") or ""),
            source_campaign_id=str(data.get("source_campaign_id") or ""),
        )


@dataclass(frozen=True)
class ComparisonCell:
    historical: str
    current: str
    classification: ReplayObservationClass = ReplayObservationClass.HISTORICAL_REPRODUCTION

    def as_dict(self) -> dict[str, Any]:
        return {
            "historical": self.historical,
            "current": self.current,
            "classification": self.classification.value,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ComparisonCell:
        return cls(
            historical=str(data.get("historical") or ""),
            current=str(data.get("current") or ""),
            classification=ReplayObservationClass(
                data.get("classification") or ReplayObservationClass.HISTORICAL_REPRODUCTION.value
            ),
        )


@dataclass(frozen=True)
class ReplayComparison:
    source_target_id: str
    replay_campaign_id: str
    dimensions: dict[str, ComparisonCell] = field(default_factory=dict)
    v2_4_added_information: tuple[str, ...] = ()
    v2_4_regression: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_target_id": self.source_target_id,
            "replay_campaign_id": self.replay_campaign_id,
            "dimensions": {key: value.as_dict() for key, value in self.dimensions.items()},
            "v2_4_added_information": list(self.v2_4_added_information),
            "v2_4_regression": list(self.v2_4_regression),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ReplayComparison:
        raw = data.get("dimensions") or {}
        return cls(
            source_target_id=str(data.get("source_target_id") or ""),
            replay_campaign_id=str(data.get("replay_campaign_id") or ""),
            dimensions={str(key): ComparisonCell.from_dict(value) for key, value in dict(raw).items()},
            v2_4_added_information=tuple(str(item) for item in (data.get("v2_4_added_information") or ())),
            v2_4_regression=tuple(str(item) for item in (data.get("v2_4_regression") or ())),
        )


@dataclass(frozen=True)
class CampaignControlRecord:
    """v2.4 overlay record. Does not mutate MemoryExperiment."""

    campaign_id: str
    experiment_id: str
    target: str
    execution_status: ExecutionStatus
    mathematical_status: MathematicalStatus
    proposals: AttackProposalDossier
    close_tag: CloseTag | None = None
    provenance: dict[str, FieldProvenance] = field(default_factory=dict)
    campaign_type: CampaignType = CampaignType.LIVE
    replay_metadata: ReplayMetadata | None = None
    comparison: ReplayComparison | None = None
    engine_control_version: str = ENGINE_CONTROL_VERSION
    source_engine_version: str = ""
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "experiment_id": self.experiment_id,
            "target": self.target,
            "execution_status": self.execution_status.value,
            "mathematical_status": self.mathematical_status.value,
            "close_tag": None if self.close_tag is None else self.close_tag.value,
            "provenance": {key: value.value for key, value in self.provenance.items()},
            "proposals": self.proposals.as_dict(),
            "campaign_type": self.campaign_type.value,
            "replay_metadata": None if self.replay_metadata is None else self.replay_metadata.as_dict(),
            "comparison": None if self.comparison is None else self.comparison.as_dict(),
            "engine_control_version": self.engine_control_version,
            "source_engine_version": self.source_engine_version,
            "notes": list(self.notes),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CampaignControlRecord:
        raw_close = data.get("close_tag")
        raw_replay = data.get("replay_metadata")
        raw_cmp = data.get("comparison")
        raw_prov = data.get("provenance") or {}
        return cls(
            campaign_id=str(data["campaign_id"]),
            experiment_id=str(data.get("experiment_id") or data["campaign_id"]),
            target=str(data.get("target") or ""),
            execution_status=ExecutionStatus(data["execution_status"]),
            mathematical_status=MathematicalStatus(data["mathematical_status"]),
            proposals=AttackProposalDossier.from_dict(data.get("proposals") or {"proposals": []}),
            close_tag=None if not raw_close else CloseTag(raw_close),
            provenance={str(key): FieldProvenance(value) for key, value in dict(raw_prov).items()},
            campaign_type=CampaignType(data.get("campaign_type") or CampaignType.LIVE.value),
            replay_metadata=None if not raw_replay else ReplayMetadata.from_dict(raw_replay),
            comparison=None if not raw_cmp else ReplayComparison.from_dict(raw_cmp),
            engine_control_version=str(data.get("engine_control_version") or ENGINE_CONTROL_VERSION),
            source_engine_version=str(data.get("source_engine_version") or ""),
            notes=tuple(str(item) for item in (data.get("notes") or ())),
        )


@dataclass(frozen=True)
class ProposalEvidence:
    """Session/memory view consumed by the non-executing proposal generator."""

    experiment_id: str
    target: str
    fingerprint: dict[str, str] = field(default_factory=dict)
    failure_classes: tuple[str, ...] = ()
    skipped_attacks: tuple[str, ...] = ()
    skip_reasons: tuple[tuple[str, str], ...] = ()
    attack_statuses: dict[str, str] = field(default_factory=dict)
    strategy_chain: str = ""
    unresolved_questions: tuple[str, ...] = ()
    new_counterexamples: tuple[str, ...] = ()
    new_obstructions: tuple[str, ...] = ()
    new_exact_results: tuple[str, ...] = ()
    known_rediscoveries: tuple[str, ...] = ()
    strongest_falsification: str = ""
    census_kind: str = ""
    piecewise_affine_structure: str = ""
    affine_control_type: str = ""
    eventual_region: str = ""
    numerical_contraction: str = ""
    decision_reason: str = ""
    novelty_status: str = ""
    lean_certificate: str = ""
    computation_exhausted: bool = False
    infinite_reachability_unresolved: bool = False


@dataclass(frozen=True)
class RetrospectiveReport:
    successful_capabilities: tuple[str, ...]
    recurring_failure_modes: tuple[str, ...]
    recurring_missing_capabilities: tuple[tuple[str, int], ...]
    campaign_ids: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "successful_capabilities": list(self.successful_capabilities),
            "recurring_failure_modes": list(self.recurring_failure_modes),
            "recurring_missing_capabilities": [
                {"capability": name, "count": count} for name, count in self.recurring_missing_capabilities
            ],
            "campaign_ids": list(self.campaign_ids),
            "notes": list(self.notes),
        }


__all__ = [
    "BASELINE_IDENTIFIER",
    "COMPARISON_DIMENSIONS",
    "CampaignControlRecord",
    "CampaignType",
    "CloseTag",
    "ComparisonCell",
    "Confidence",
    "ControlSchemaError",
    "ENGINE_CONTROL_VERSION",
    "EXECUTION_ENGINE",
    "ExecutionStatus",
    "FORBIDDEN_PROPOSAL_NAMES",
    "FieldProvenance",
    "ImplementationScope",
    "MathematicalStatus",
    "NoveltyRisk",
    "ProposalEvidence",
    "REPLAY_V22_TARGETS",
    "ReplayComparison",
    "ReplayMetadata",
    "ReplayObservationClass",
    "RetrospectiveReport",
    "STRONG_MATHEMATICAL_YIELD",
    "V2_3_CAMPAIGN_ORDER",
    "AttackProposal",
    "AttackProposalDossier",
]
