"""v2.3 Phase 1 strategy types. Not attack objects and not a theorem ledger."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from enum import Enum
from typing import Any, Mapping

from research_engine.attacks.result import AttackResult
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.memory.types import NoveltyStatus
from research_engine.planner.orchestrator import SkipRecord

ENGINE_STRATEGY_VERSION = "0.2.3"

MappingLike = Mapping[str, Any]


class ResearchGoal(str, Enum):
    ORIGIN_AVOIDANCE = "ORIGIN_AVOIDANCE"
    TERMINATION = "TERMINATION"
    CYCLE_EXCLUSION = "CYCLE_EXCLUSION"
    POSITIVITY = "POSITIVITY"
    REACHABILITY = "REACHABILITY"
    BOUNDEDNESS = "BOUNDEDNESS"


class ResearchHypothesisStatus(str, Enum):
    """Engine hypothesis life-cycle. Not a theorem-ledger tag."""

    CANDIDATE = "CANDIDATE"
    REFUTED = "REFUTED"
    SEARCH_SUPPORTED = "SEARCH_SUPPORTED"
    PROOF_READY = "PROOF_READY"
    PROVED = "PROVED"
    LEAN_CERTIFIED = "LEAN_CERTIFIED"


class ObligationKind(str, Enum):
    INDUCTIVE_INCLUSION = "INDUCTIVE_INCLUSION"
    DOMAIN_CERTIFICATION = "DOMAIN_CERTIFICATION"
    DIVISIBILITY = "DIVISIBILITY"
    MATRIX_INVARIANT = "MATRIX_INVARIANT"
    RANKING_DESCENT = "RANKING_DESCENT"
    CLASS_OBSTRUCTION = "CLASS_OBSTRUCTION"
    CONTROL_COMPOSITION = "CONTROL_COMPOSITION"


@dataclass(frozen=True)
class ProofObligation:
    kind: ObligationKind
    statement: str
    status: str = "OPEN"

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "statement": self.statement,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> ProofObligation:
        return cls(
            kind=ObligationKind(data["kind"]),
            statement=str(data.get("statement") or ""),
            status=str(data.get("status") or "OPEN"),
        )


@dataclass(frozen=True)
class ResearchHypothesis:
    """Persistent research hypothesis. Distinct from session ``Hypothesis``."""

    id: str
    statement: str
    target: str
    source_target: str
    evidence: str = ""
    supporting_artifacts: tuple[str, ...] = ()
    counterexamples: tuple[str, ...] = ()
    confidence: float = 0.0
    current_status: ResearchHypothesisStatus = ResearchHypothesisStatus.CANDIDATE
    closest_known_result: str = ""
    prior_art_matches: tuple[str, ...] = ()
    proof_obligations: tuple[ProofObligation, ...] = ()
    candidate_attack_chain: tuple[str, ...] = ()
    expected_value: float = 0.0
    failure_learning_value: float = 1.0
    novelty_status: NoveltyStatus = NoveltyStatus.UNKNOWN
    cluster_id: str = ""
    goal: ResearchGoal | None = None
    kind: ClaimKind = ClaimKind.REACHABLE
    intended_scope: SearchScope = SearchScope.BOUNDED

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "statement": self.statement,
            "target": self.target,
            "source_target": self.source_target,
            "evidence": self.evidence,
            "supporting_artifacts": list(self.supporting_artifacts),
            "counterexamples": list(self.counterexamples),
            "confidence": self.confidence,
            "current_status": self.current_status.value,
            "closest_known_result": self.closest_known_result,
            "prior_art_matches": list(self.prior_art_matches),
            "proof_obligations": [item.as_dict() for item in self.proof_obligations],
            "candidate_attack_chain": list(self.candidate_attack_chain),
            "expected_value": self.expected_value,
            "failure_learning_value": self.failure_learning_value,
            "novelty_status": self.novelty_status.value,
            "cluster_id": self.cluster_id,
            "goal": None if self.goal is None else self.goal.value,
            "kind": self.kind.value,
            "intended_scope": self.intended_scope.value,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> ResearchHypothesis:
        raw_goal = data.get("goal")
        return cls(
            id=str(data["id"]),
            statement=str(data.get("statement") or ""),
            target=str(data.get("target") or ""),
            source_target=str(data.get("source_target") or data.get("target") or ""),
            evidence=str(data.get("evidence") or ""),
            supporting_artifacts=tuple(str(item) for item in (data.get("supporting_artifacts") or ())),
            counterexamples=tuple(str(item) for item in (data.get("counterexamples") or ())),
            confidence=float(data.get("confidence") or 0.0),
            current_status=ResearchHypothesisStatus(
                data.get("current_status") or ResearchHypothesisStatus.CANDIDATE.value
            ),
            closest_known_result=str(data.get("closest_known_result") or ""),
            prior_art_matches=tuple(str(item) for item in (data.get("prior_art_matches") or ())),
            proof_obligations=tuple(
                ProofObligation.from_dict(item) for item in (data.get("proof_obligations") or ())
            ),
            candidate_attack_chain=tuple(
                str(item) for item in (data.get("candidate_attack_chain") or ())
            ),
            expected_value=float(data.get("expected_value") or 0.0),
            failure_learning_value=float(data.get("failure_learning_value") or 1.0),
            novelty_status=NoveltyStatus(data.get("novelty_status") or NoveltyStatus.UNKNOWN.value),
            cluster_id=str(data.get("cluster_id") or ""),
            goal=None if not raw_goal else ResearchGoal(raw_goal),
            kind=ClaimKind(data.get("kind") or ClaimKind.REACHABLE.value),
            intended_scope=SearchScope(data.get("intended_scope") or SearchScope.BOUNDED.value),
        )


@dataclass(frozen=True)
class AttackCapability:
    name: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    preconditions: tuple[str, ...] = ()
    evidence_requirements: tuple[str, ...] = ()
    cost: float = 1.0
    known_failure_modes: tuple[str, ...] = ()
    goals_served: tuple[ResearchGoal, ...] = ()
    recommended_next: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "preconditions": list(self.preconditions),
            "evidence_requirements": list(self.evidence_requirements),
            "cost": self.cost,
            "known_failure_modes": list(self.known_failure_modes),
            "goals_served": [item.value for item in self.goals_served],
            "recommended_next": list(self.recommended_next),
        }


@dataclass(frozen=True)
class AttackChain:
    id: str
    attacks: tuple[str, ...]
    goals: tuple[ResearchGoal, ...]
    expected_outputs: tuple[str, ...] = ()
    historical_yield: float = 1.0
    cost: float = 1.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "attacks": list(self.attacks),
            "goals": [item.value for item in self.goals],
            "expected_outputs": list(self.expected_outputs),
            "historical_yield": self.historical_yield,
            "cost": self.cost,
        }


@dataclass(frozen=True)
class StrategyPlan:
    goal: ResearchGoal
    chain: AttackChain
    alternatives: tuple[AttackChain, ...] = ()
    reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal.value,
            "chain": self.chain.as_dict(),
            "alternatives": [item.as_dict() for item in self.alternatives],
            "reason": self.reason,
        }


@dataclass(frozen=True)
class StrategyMetrics:
    mathematical_yield: float = 0.0
    engineering_cost: float = 0.0
    strategy_efficiency: float = 0.0
    hypothesis_yield: float = 0.0
    proof_conversion: float = 0.0
    attack_chain_efficiency: float = 0.0
    attacks_executed: int = 0
    useful_results: int = 0
    generated_hypotheses: int = 0
    surviving_hypotheses: int = 0

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StrategyReport:
    plan: StrategyPlan
    results: tuple[AttackResult, ...]
    skipped: tuple[SkipRecord, ...] = ()
    hypotheses: tuple[ResearchHypothesis, ...] = ()
    metrics: StrategyMetrics = field(default_factory=StrategyMetrics)
    attempted_chains: tuple[str, ...] = ()
    version: str = ENGINE_STRATEGY_VERSION

    def replace(self, **changes: Any) -> StrategyReport:
        return replace(self, **changes)
