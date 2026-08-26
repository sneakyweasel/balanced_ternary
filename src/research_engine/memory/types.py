"""Research-memory types. Not attack objects and not a theorem ledger."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from enum import Enum
from typing import Any

from research_engine.diagnosis.types import (
    CapabilityCoverage,
    ExperimentRecord,
    FamilyStatus,
    RegimeFingerprint,
    ResearchDecision,
    StructuralDelta,
)

ENGINE_MEMORY_VERSION = "0.2.2"


class MemoryLane(str, Enum):
    """Isolation lanes. Scout and grey loot never enter a blind attack."""

    SCOUT = "scout"
    ATTACK = "attack"
    GREY_LOOT = "grey_loot"
    CERTIFIED = "certified"


class FailureClass(str, Enum):
    """What a failure means mathematically. Not merely attack=FAIL."""

    REPRESENTATION = "REPRESENTATION"
    DISCOVERY = "DISCOVERY"
    DOMAIN_INFERENCE = "DOMAIN_INFERENCE"
    CERTIFICATION = "CERTIFICATION"
    COMPOSITION = "COMPOSITION"
    QUANTIFIER = "QUANTIFIER"
    REACHABILITY = "REACHABILITY"
    OBSTRUCTION = "OBSTRUCTION"
    GLOBAL_REASONING = "GLOBAL_REASONING"
    PROOF = "PROOF"
    COMPUTATIONAL = "COMPUTATIONAL"
    EXPERIMENT_HYGIENE = "EXPERIMENT_HYGIENE"
    PRIOR_ART = "PRIOR_ART"
    NOVELTY = "NOVELTY"


FAILURE_CLASS_DEFINITIONS: dict[FailureClass, str] = {
    FailureClass.REPRESENTATION: (
        "The target's mathematical structure cannot be represented naturally "
        "by the current engine language. Example: n |-> sigma(n)-n."
    ),
    FailureClass.DISCOVERY: (
        "A candidate structure was proposed but not recovered from exact I/O, "
        "or the recovered structure is not the intended one."
    ),
    FailureClass.DOMAIN_INFERENCE: (
        "Region or domain inference truncates or mis-partitions a law that is "
        "globally valid. Example: sign-first involution census."
    ),
    FailureClass.CERTIFICATION: (
        "A reconstructed relation exists on a sample but the arithmetic domain "
        "is not certified as exact."
    ),
    FailureClass.COMPOSITION: (
        "Local certified pieces exist but symbolic multi-step composition is "
        "missing or inapplicable."
    ),
    FailureClass.QUANTIFIER: (
        "The target requires existential, universal, or mixed reasoning not "
        "consumed by the current deterministic control language. Example: "
        "genuinely nondeterministic SLCs."
    ),
    FailureClass.REACHABILITY: (
        "Finite or bounded reachability failed, was truncated, or was mistaken "
        "for an infinite-time statement."
    ),
    FailureClass.OBSTRUCTION: (
        "An obstruction calculus was applicable in principle but produced no "
        "class- or word-level contradiction."
    ),
    FailureClass.GLOBAL_REASONING: (
        "The representation is adequate, but the engine cannot bridge "
        "finite/local evidence to an infinite-time theorem. Example: order-6 "
        "Skolem zero reachability."
    ),
    FailureClass.PROOF: (
        "An exact computational identity exists but has no Lean certificate, "
        "or the formalization obligation is out of scope."
    ),
    FailureClass.COMPUTATIONAL: (
        "Exact reasoning is conceptually available but computationally blocked. "
        "Not mathematical impossibility."
    ),
    FailureClass.EXPERIMENT_HYGIENE: (
        "The experiment or its benchmark protocol was flawed, including false "
        "literature-leak failures on identifiers."
    ),
    FailureClass.PRIOR_ART: (
        "Reconciliation failed to distinguish keyword overlap from semantic "
        "equivalence, or known status was mis-tagged."
    ),
    FailureClass.NOVELTY: (
        "The run rediscovered a saturated or known regime and produced no new "
        "mathematical output."
    ),
}


class LootEvidence(str, Enum):
    """Evidence status of a grey-loot item. Not a theorem-ledger tag."""

    OBSERVED = "OBSERVED"
    FINITE_RANGE = "FINITE_RANGE"
    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    PROVED = "PROVED"
    KNOWN = "KNOWN"
    CONJECTURAL = "CONJECTURAL"


class GreyLootKind(str, Enum):
    COUNTEREXAMPLE = "Counterexample"
    FAILED_INVARIANT = "Failed invariant"
    CANDIDATE_INVARIANT = "Candidate invariant"
    FAILED_DOMAIN_PREDICATE = "Failed domain predicate"
    LATENT_CONTROL_PATTERN = "Latent control pattern"
    BRANCH_PATTERN = "Branch pattern"
    OBSTRUCTION_PATTERN = "Obstruction pattern"
    REPRESENTATION_MISMATCH = "Representation mismatch"
    QUANTIFIER_MISMATCH = "Quantifier mismatch"
    USEFUL_NEGATIVE_RESULT = "Useful negative result"
    PRIOR_ART_TERMINOLOGY = "Prior-art terminology"
    COMPLEXITY_OBSERVATION = "Complexity observation"
    COMPUTATIONAL_BOTTLENECK = "Computational bottleneck"
    POTENTIAL_TARGET_TRANSFORMATION = "Potential target transformation"
    POTENTIAL_RESEARCH_QUESTION = "Potential research question"


class NoveltyLevel(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class NoveltyStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    KNOWN_REDISCOVERY = "KNOWN_REDISCOVERY"
    NEW_FORMULATION = "NEW_FORMULATION"
    PROJECT_SPECIFIC = "PROJECT_SPECIFIC"
    OPEN = "OPEN"


class DecisionReason(str, Enum):
    """Structured reason alongside ResearchDecision. Does not replace it."""

    NONE = "NONE"
    KNOWN_REDISCOVERY = "KNOWN_REDISCOVERY"
    LOW_MATHEMATICAL_YIELD = "LOW_MATHEMATICAL_YIELD"
    RECURRING_ENGINE_LIMITATION = "RECURRING_ENGINE_LIMITATION"
    FAMILY_SATURATED = "FAMILY_SATURATED"
    EXPERIMENT_HYGIENE = "EXPERIMENT_HYGIENE"
    REPRESENTATION_MISMATCH = "REPRESENTATION_MISMATCH"
    QUANTIFIER_MISMATCH = "QUANTIFIER_MISMATCH"
    GLOBAL_REACHABILITY_GAP = "GLOBAL_REACHABILITY_GAP"
    COMPUTATIONAL_BUDGET = "COMPUTATIONAL_BUDGET"
    DISTINCT_REGIME = "DISTINCT_REGIME"
    SALVAGED_LANGUAGE = "SALVAGED_LANGUAGE"


class FailureStatus(str, Enum):
    OPEN = "OPEN"
    PARKED = "PARKED"
    RESOLVED = "RESOLVED"
    RECORDED = "RECORDED"


class ImportanceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class EngineeringRecommendation(str, Enum):
    IGNORE = "IGNORE"
    PARK = "PARK"
    WATCH = "WATCH"
    PROTOTYPE = "PROTOTYPE"
    PROTOTYPE_LATER = "PROTOTYPE_LATER"
    PROMOTE_TO_NEXT_VERSION = "PROMOTE_TO_NEXT_VERSION"


class ClusterDecision(str, Enum):
    IGNORE = "IGNORE"
    PARK = "PARK"
    WATCH = "WATCH"
    RECORD = "RECORD"


class GreyLootStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PARKED = "PARKED"
    REFUTED = "REFUTED"
    REUSED = "REUSED"
    SATURATED = "SATURATED"
    SUPERSEDED = "SUPERSEDED"


class TargetPool(str, Enum):
    CALIBRATION = "CALIBRATION"
    FRONTIER = "FRONTIER"
    WILDCARD = "WILDCARD"


@dataclass(frozen=True)
class GreyLoot:
    id: str
    kind: GreyLootKind
    statement: str
    evidence: LootEvidence
    experiment_id: str
    target: str = ""
    failure_class: FailureClass | None = None
    bottleneck: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    observation: str = ""
    minimal_example: str = ""
    counterexample: str = ""
    reusable_lesson: str = ""
    possible_transfer_targets: tuple[str, ...] = ()
    prior_art_status: str = ""
    engineering_action: str = ""
    status: GreyLootStatus = GreyLootStatus.PARKED

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind.value,
            "statement": self.statement,
            "evidence": self.evidence.value,
            "experiment_id": self.experiment_id,
            "target": self.target,
            "failure_class": None if self.failure_class is None else self.failure_class.value,
            "bottleneck": self.bottleneck,
            "payload": dict(self.payload),
            "observation": self.observation,
            "minimal_example": self.minimal_example,
            "counterexample": self.counterexample,
            "reusable_lesson": self.reusable_lesson,
            "possible_transfer_targets": list(self.possible_transfer_targets),
            "prior_art_status": self.prior_art_status,
            "engineering_action": self.engineering_action,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> GreyLoot:
        raw_class = data.get("failure_class")
        raw_status = data.get("status")
        return cls(
            id=str(data["id"]),
            kind=GreyLootKind(data["kind"]),
            statement=str(data["statement"]),
            evidence=LootEvidence(data["evidence"]),
            experiment_id=str(data["experiment_id"]),
            target=str(data.get("target") or ""),
            failure_class=None if not raw_class else FailureClass(raw_class),
            bottleneck=str(data.get("bottleneck") or ""),
            payload=dict(data.get("payload") or {}),
            observation=str(data.get("observation") or ""),
            minimal_example=str(data.get("minimal_example") or ""),
            counterexample=str(data.get("counterexample") or ""),
            reusable_lesson=str(data.get("reusable_lesson") or ""),
            possible_transfer_targets=tuple(
                str(item) for item in (data.get("possible_transfer_targets") or ())
            ),
            prior_art_status=str(data.get("prior_art_status") or ""),
            engineering_action=str(data.get("engineering_action") or ""),
            status=GreyLootStatus(raw_status) if raw_status else GreyLootStatus.PARKED,
        )


@dataclass(frozen=True)
class FailureRecord:
    id: str
    target: str
    experiment_id: str
    engine_version: str
    phase: str
    attack: str
    failure_class: FailureClass
    representation_status: str
    mathematical_bottleneck: str
    evidence: str
    counterexamples: tuple[str, ...] = ()
    minimal_example: str = ""
    reproducibility: str = "seed"
    reusable_lesson: str = ""
    prior_art_status: str = ""
    engineering_action: str = "PARK"
    research_value: ImportanceLevel = ImportanceLevel.MEDIUM
    status: FailureStatus = FailureStatus.RECORDED
    affected_attack_family: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "target": self.target,
            "experiment_id": self.experiment_id,
            "engine_version": self.engine_version,
            "phase": self.phase,
            "attack": self.attack,
            "failure_class": self.failure_class.value,
            "representation_status": self.representation_status,
            "mathematical_bottleneck": self.mathematical_bottleneck,
            "evidence": self.evidence,
            "counterexamples": list(self.counterexamples),
            "minimal_example": self.minimal_example,
            "reproducibility": self.reproducibility,
            "reusable_lesson": self.reusable_lesson,
            "prior_art_status": self.prior_art_status,
            "engineering_action": self.engineering_action,
            "research_value": self.research_value.value,
            "status": self.status.value,
            "affected_attack_family": self.affected_attack_family,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> FailureRecord:
        return cls(
            id=str(data["id"]),
            target=str(data["target"]),
            experiment_id=str(data["experiment_id"]),
            engine_version=str(data.get("engine_version") or ENGINE_MEMORY_VERSION),
            phase=str(data.get("phase") or ""),
            attack=str(data.get("attack") or ""),
            failure_class=FailureClass(data["failure_class"]),
            representation_status=str(data.get("representation_status") or ""),
            mathematical_bottleneck=str(data.get("mathematical_bottleneck") or ""),
            evidence=str(data.get("evidence") or ""),
            counterexamples=tuple(str(item) for item in (data.get("counterexamples") or ())),
            minimal_example=str(data.get("minimal_example") or ""),
            reproducibility=str(data.get("reproducibility") or "seed"),
            reusable_lesson=str(data.get("reusable_lesson") or ""),
            prior_art_status=str(data.get("prior_art_status") or ""),
            engineering_action=str(data.get("engineering_action") or "PARK"),
            research_value=ImportanceLevel(data.get("research_value") or ImportanceLevel.MEDIUM.value),
            status=FailureStatus(data.get("status") or FailureStatus.RECORDED.value),
            affected_attack_family=str(data.get("affected_attack_family") or data.get("attack") or ""),
        )

    def cluster_key(self) -> tuple[str, str, str, str]:
        family = self.affected_attack_family or self.attack
        return (
            self.failure_class.value,
            self.representation_status,
            self.mathematical_bottleneck,
            family,
        )


@dataclass(frozen=True)
class MathematicalYield:
    known_rediscoveries: tuple[str, ...] = ()
    new_exact_results: tuple[str, ...] = ()
    new_formalizations: tuple[str, ...] = ()
    new_counterexamples: tuple[str, ...] = ()
    new_conjectures: tuple[str, ...] = ()
    new_obstructions: tuple[str, ...] = ()
    new_reductions: tuple[str, ...] = ()
    new_classifications: tuple[str, ...] = ()
    new_terminology: tuple[str, ...] = ()
    potentially_new_mathematics: tuple[str, ...] = ()
    unresolved_questions: tuple[str, ...] = ()
    engineering_changes: int = 0

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: MappingLike) -> MathematicalYield:
        def _words(name: str) -> tuple[str, ...]:
            return tuple(str(item) for item in (data.get(name) or ()))

        return cls(
            known_rediscoveries=_words("known_rediscoveries"),
            new_exact_results=_words("new_exact_results"),
            new_formalizations=_words("new_formalizations"),
            new_counterexamples=_words("new_counterexamples"),
            new_conjectures=_words("new_conjectures"),
            new_obstructions=_words("new_obstructions"),
            new_reductions=_words("new_reductions"),
            new_classifications=_words("new_classifications"),
            new_terminology=_words("new_terminology"),
            potentially_new_mathematics=_words("potentially_new_mathematics"),
            unresolved_questions=_words("unresolved_questions"),
            engineering_changes=int(data.get("engineering_changes") or 0),
        )


@dataclass(frozen=True)
class KnownEquivalent:
    known_equivalent: bool
    engine_form: str
    mathematical_meaning: str
    literature_id: str = ""
    confidence: str = "high"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: MappingLike) -> KnownEquivalent:
        return cls(
            known_equivalent=bool(data.get("known_equivalent")),
            engine_form=str(data.get("engine_form") or ""),
            mathematical_meaning=str(data.get("mathematical_meaning") or ""),
            literature_id=str(data.get("literature_id") or ""),
            confidence=str(data.get("confidence") or "high"),
        )


@dataclass(frozen=True)
class PriorArtMemory:
    literature_ids: tuple[str, ...] = ()
    semantic_equivalents: tuple[KnownEquivalent, ...] = ()
    terminology_variants: tuple[str, ...] = ()
    known_theorem_status: str = ""
    publication_date: str = ""
    confidence: str = ""
    independently_rediscovered: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "literature_ids": list(self.literature_ids),
            "semantic_equivalents": [item.as_dict() for item in self.semantic_equivalents],
            "terminology_variants": list(self.terminology_variants),
            "known_theorem_status": self.known_theorem_status,
            "publication_date": self.publication_date,
            "confidence": self.confidence,
            "independently_rediscovered": self.independently_rediscovered,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> PriorArtMemory:
        equiv = tuple(
            KnownEquivalent.from_dict(item) for item in (data.get("semantic_equivalents") or ())
        )
        return cls(
            literature_ids=tuple(str(item) for item in (data.get("literature_ids") or ())),
            semantic_equivalents=equiv,
            terminology_variants=tuple(str(item) for item in (data.get("terminology_variants") or ())),
            known_theorem_status=str(data.get("known_theorem_status") or ""),
            publication_date=str(data.get("publication_date") or ""),
            confidence=str(data.get("confidence") or ""),
            independently_rediscovered=bool(data.get("independently_rediscovered")),
        )


@dataclass(frozen=True)
class ScoutDossier:
    target: str
    problem_definition: str = ""
    literature: tuple[str, ...] = ()
    known_results: tuple[str, ...] = ()
    open_questions: str = ""
    saturation: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "problem_definition": self.problem_definition,
            "literature": list(self.literature),
            "known_results": list(self.known_results),
            "open_questions": self.open_questions,
            "saturation": self.saturation,
            "extra": dict(self.extra),
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> ScoutDossier:
        return cls(
            target=str(data["target"]),
            problem_definition=str(data.get("problem_definition") or ""),
            literature=tuple(str(item) for item in (data.get("literature") or ())),
            known_results=tuple(str(item) for item in (data.get("known_results") or ())),
            open_questions=str(data.get("open_questions") or ""),
            saturation=str(data.get("saturation") or ""),
            extra=dict(data.get("extra") or {}),
        )


@dataclass(frozen=True)
class BlindPacket:
    """Attack-lane input. Must not carry scout or grey-loot fields."""

    spec_name: str
    dimension: int | None = None
    skip_attacks: tuple[str, ...] = ()
    max_states: int | None = None
    max_steps: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)
    allowed_definition: str = ""
    state_space: str = ""
    observation: str = ""
    initial_conditions: tuple[str, ...] = ()
    explicit_controls: str = ""
    computational_budget: str = ""
    forbidden_hints: tuple[str, ...] = ()
    post_run_reconciliation: str = ""
    lean_targets: tuple[str, ...] = ()

    def attack_payload(self) -> dict[str, Any]:
        """Engine-visible fields. Forbidden-hint lists are metadata, not I/O."""

        return {
            "spec_name": self.spec_name,
            "dimension": self.dimension,
            "skip_attacks": list(self.skip_attacks),
            "max_states": self.max_states,
            "max_steps": self.max_steps,
            "allowed_definition": self.allowed_definition,
            "state_space": self.state_space,
            "observation": self.observation,
            "initial_conditions": list(self.initial_conditions),
            "explicit_controls": self.explicit_controls,
            "computational_budget": self.computational_budget,
        }

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.attack_payload(),
            "extra": dict(self.extra),
            "forbidden_hints": list(self.forbidden_hints),
            "post_run_reconciliation": self.post_run_reconciliation,
            "lean_targets": list(self.lean_targets),
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> BlindPacket:
        extra = dict(data.get("extra") or {})
        forbidden = {
            "scout",
            "grey_loot",
            "literature",
            "known_results",
            "hypotheses",
            "research_hypothesis",
            "known_theorem_status",
            "prior_art",
        }
        extra = {key: value for key, value in extra.items() if key not in forbidden}
        return cls(
            spec_name=str(data["spec_name"]),
            dimension=data.get("dimension"),
            skip_attacks=tuple(str(item) for item in (data.get("skip_attacks") or ())),
            max_states=data.get("max_states"),
            max_steps=data.get("max_steps"),
            extra=extra,
            allowed_definition=str(data.get("allowed_definition") or ""),
            state_space=str(data.get("state_space") or ""),
            observation=str(data.get("observation") or ""),
            initial_conditions=tuple(str(item) for item in (data.get("initial_conditions") or ())),
            explicit_controls=str(data.get("explicit_controls") or ""),
            computational_budget=str(data.get("computational_budget") or ""),
            forbidden_hints=tuple(str(item) for item in (data.get("forbidden_hints") or ())),
            post_run_reconciliation=str(data.get("post_run_reconciliation") or ""),
            lean_targets=tuple(str(item) for item in (data.get("lean_targets") or ())),
        )


@dataclass(frozen=True)
class RunArtifact:
    attack_statuses: dict[str, str] = field(default_factory=dict)
    skipped: tuple[str, ...] = ()
    strongest_exact: str = ""
    strongest_falsification: str = ""
    census_kind: str = ""
    lean_theorems: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "attack_statuses": dict(self.attack_statuses),
            "skipped": list(self.skipped),
            "strongest_exact": self.strongest_exact,
            "strongest_falsification": self.strongest_falsification,
            "census_kind": self.census_kind,
            "lean_theorems": list(self.lean_theorems),
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> RunArtifact:
        return cls(
            attack_statuses={str(k): str(v) for k, v in dict(data.get("attack_statuses") or {}).items()},
            skipped=tuple(str(item) for item in (data.get("skipped") or ())),
            strongest_exact=str(data.get("strongest_exact") or ""),
            strongest_falsification=str(data.get("strongest_falsification") or ""),
            census_kind=str(data.get("census_kind") or ""),
            lean_theorems=tuple(str(item) for item in (data.get("lean_theorems") or ())),
        )


@dataclass(frozen=True)
class Reconciliation:
    notes: str = ""
    prior_art: PriorArtMemory | None = None
    novelty_status: NoveltyStatus = NoveltyStatus.UNKNOWN
    independently_rediscovered: bool | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "notes": self.notes,
            "prior_art": None if self.prior_art is None else self.prior_art.as_dict(),
            "novelty_status": self.novelty_status.value,
            "independently_rediscovered": self.independently_rediscovered,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> Reconciliation:
        raw = data.get("prior_art")
        return cls(
            notes=str(data.get("notes") or ""),
            prior_art=None if not raw else PriorArtMemory.from_dict(raw),
            novelty_status=NoveltyStatus(data.get("novelty_status") or NoveltyStatus.UNKNOWN.value),
            independently_rediscovered=data.get("independently_rediscovered"),
        )


@dataclass(frozen=True)
class ResearchQuestion:
    id: str
    cluster_id: str
    statement: str
    failure_class: FailureClass
    status: str = "OPEN"

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "cluster_id": self.cluster_id,
            "statement": self.statement,
            "failure_class": self.failure_class.value,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> ResearchQuestion:
        return cls(
            id=str(data["id"]),
            cluster_id=str(data["cluster_id"]),
            statement=str(data["statement"]),
            failure_class=FailureClass(data["failure_class"]),
            status=str(data.get("status") or "OPEN"),
        )


@dataclass(frozen=True)
class FailureCluster:
    id: str
    key: tuple[str, str, str, str]
    member_ids: tuple[str, ...]
    targets: tuple[str, ...]
    recurrence_count: int
    target_diversity: int
    semantic_classes: tuple[str, ...]
    mathematical_importance: ImportanceLevel
    reproducibility: str
    existing_workarounds: tuple[str, ...] = ()
    suggested_future_abstraction: str = ""
    current_decision: ClusterDecision = ClusterDecision.RECORD
    research_questions: tuple[ResearchQuestion, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "key": list(self.key),
            "member_ids": list(self.member_ids),
            "targets": list(self.targets),
            "recurrence_count": self.recurrence_count,
            "target_diversity": self.target_diversity,
            "semantic_classes": list(self.semantic_classes),
            "mathematical_importance": self.mathematical_importance.value,
            "reproducibility": self.reproducibility,
            "existing_workarounds": list(self.existing_workarounds),
            "suggested_future_abstraction": self.suggested_future_abstraction,
            "current_decision": self.current_decision.value,
            "research_questions": [item.as_dict() for item in self.research_questions],
        }


@dataclass(frozen=True)
class EngineeringCandidate:
    failure_cluster: str
    recurrence_count: int
    target_diversity: int
    mathematical_importance: ImportanceLevel
    expected_research_value: ImportanceLevel
    implementation_cost: str
    reusable_scope: str
    recommendation: EngineeringRecommendation
    generic_abstraction: bool = False
    possible_generic_abstraction: str = ""
    implementation_cost_estimate: str = ""
    current_decision: EngineeringRecommendation | None = None
    reason_not_implemented: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "failure_cluster": self.failure_cluster,
            "recurrence_count": self.recurrence_count,
            "target_diversity": self.target_diversity,
            "mathematical_importance": self.mathematical_importance.value,
            "expected_research_value": self.expected_research_value.value,
            "implementation_cost": self.implementation_cost,
            "reusable_scope": self.reusable_scope,
            "recommendation": self.recommendation.value,
            "generic_abstraction": self.generic_abstraction,
            "possible_generic_abstraction": self.possible_generic_abstraction or self.reusable_scope,
            "implementation_cost_estimate": self.implementation_cost_estimate or self.implementation_cost,
            "current_decision": None
            if self.current_decision is None
            else self.current_decision.value,
            "reason_not_implemented": self.reason_not_implemented,
        }


@dataclass(frozen=True)
class EngineeringBacklogItem:
    failure_cluster: str
    evidence: str
    affected_targets: tuple[str, ...]
    proposed_abstraction: str
    expected_scope: str
    expected_research_value: ImportanceLevel
    implementation_complexity: str
    reason_not_implemented_yet: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "failure_cluster": self.failure_cluster,
            "evidence": self.evidence,
            "affected_targets": list(self.affected_targets),
            "proposed_abstraction": self.proposed_abstraction,
            "expected_scope": self.expected_scope,
            "expected_research_value": self.expected_research_value.value,
            "implementation_complexity": self.implementation_complexity,
            "reason_not_implemented_yet": self.reason_not_implemented_yet,
        }


@dataclass(frozen=True)
class MemoryExperiment:
    """Finalized research-memory record wrapping a live ExperimentRecord."""

    experiment_id: str
    target: str
    target_family: str
    adapter_version: str
    engine_version: str
    experiment_date: str
    diagnosis: ExperimentRecord
    decision_reason_code: DecisionReason = DecisionReason.NONE
    representation_novelty: NoveltyLevel = NoveltyLevel.NONE
    mathematical_novelty: NoveltyLevel = NoveltyLevel.NONE
    novelty_status: NoveltyStatus = NoveltyStatus.UNKNOWN
    mathematical_yield: MathematicalYield = field(default_factory=MathematicalYield)
    failures: tuple[FailureRecord, ...] = ()
    grey_loot: tuple[GreyLoot, ...] = ()
    prior_art: PriorArtMemory | None = None
    scout: ScoutDossier | None = None
    blind_packet: BlindPacket | None = None
    run_artifact: RunArtifact | None = None
    reconciliation: Reconciliation | None = None
    finalized: bool = False

    def finalize(self) -> MemoryExperiment:
        return replace(self, finalized=True)

    def with_reconciliation(self, overlay: Reconciliation) -> MemoryExperiment:
        if not self.finalized:
            raise RuntimeError("reconciliation is allowed only after finalize")
        return replace(self, reconciliation=overlay)

    def as_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "target": self.target,
            "target_family": self.target_family,
            "adapter_version": self.adapter_version,
            "engine_version": self.engine_version,
            "experiment_date": self.experiment_date,
            "diagnosis": experiment_record_to_dict(self.diagnosis),
            "decision_reason_code": self.decision_reason_code.value,
            "representation_novelty": self.representation_novelty.value,
            "mathematical_novelty": self.mathematical_novelty.value,
            "novelty_status": self.novelty_status.value,
            "mathematical_yield": self.mathematical_yield.as_dict(),
            "failures": [item.as_dict() for item in self.failures],
            "grey_loot": [item.as_dict() for item in self.grey_loot],
            "prior_art": None if self.prior_art is None else self.prior_art.as_dict(),
            "scout": None if self.scout is None else self.scout.as_dict(),
            "blind_packet": None if self.blind_packet is None else self.blind_packet.as_dict(),
            "run_artifact": None if self.run_artifact is None else self.run_artifact.as_dict(),
            "reconciliation": None if self.reconciliation is None else self.reconciliation.as_dict(),
            "finalized": self.finalized,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> MemoryExperiment:
        raw_prior = data.get("prior_art")
        raw_scout = data.get("scout")
        raw_blind = data.get("blind_packet")
        raw_run = data.get("run_artifact")
        raw_recon = data.get("reconciliation")
        return cls(
            experiment_id=str(data["experiment_id"]),
            target=str(data["target"]),
            target_family=str(data.get("target_family") or ""),
            adapter_version=str(data.get("adapter_version") or ""),
            engine_version=str(data.get("engine_version") or ENGINE_MEMORY_VERSION),
            experiment_date=str(data.get("experiment_date") or ""),
            diagnosis=experiment_record_from_dict(data["diagnosis"]),
            decision_reason_code=DecisionReason(
                data.get("decision_reason_code") or DecisionReason.NONE.value
            ),
            representation_novelty=NoveltyLevel(
                data.get("representation_novelty") or NoveltyLevel.NONE.value
            ),
            mathematical_novelty=NoveltyLevel(
                data.get("mathematical_novelty") or NoveltyLevel.NONE.value
            ),
            novelty_status=NoveltyStatus(data.get("novelty_status") or NoveltyStatus.UNKNOWN.value),
            mathematical_yield=MathematicalYield.from_dict(data.get("mathematical_yield") or {}),
            failures=tuple(FailureRecord.from_dict(item) for item in (data.get("failures") or ())),
            grey_loot=tuple(GreyLoot.from_dict(item) for item in (data.get("grey_loot") or ())),
            prior_art=None if not raw_prior else PriorArtMemory.from_dict(raw_prior),
            scout=None if not raw_scout else ScoutDossier.from_dict(raw_scout),
            blind_packet=None if not raw_blind else BlindPacket.from_dict(raw_blind),
            run_artifact=None if not raw_run else RunArtifact.from_dict(raw_run),
            reconciliation=None if not raw_recon else Reconciliation.from_dict(raw_recon),
            finalized=bool(data.get("finalized")),
        )


@dataclass(frozen=True)
class ScoredAxis:
    """Numeric score plus the reason it is not arbitrary."""

    value: float
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {"value": self.value, "reason": self.reason}

    @classmethod
    def from_dict(cls, data: MappingLike | float | int) -> ScoredAxis:
        if isinstance(data, (int, float)):
            return cls(value=float(data), reason="")
        return cls(value=float(data.get("value") or 0.0), reason=str(data.get("reason") or ""))


@dataclass(frozen=True)
class PriorArtDossier:
    """Scout-lane prior-art map. Never copied into a BlindPacket."""

    target: str
    definition: str = ""
    known_equivalent_formulations: tuple[str, ...] = ()
    known_theorems: tuple[str, ...] = ()
    known_conjectures: tuple[str, ...] = ()
    known_counterexamples: tuple[str, ...] = ()
    known_computational_results: tuple[str, ...] = ()
    known_methods: tuple[str, ...] = ()
    known_barriers: tuple[str, ...] = ()
    open_question: str = ""
    open_question_confidence: str = ""
    current_literature_activity: str = ""
    last_checked: str = "2026-08-25"
    literature_ids: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "definition": self.definition,
            "known_equivalent_formulations": list(self.known_equivalent_formulations),
            "known_theorems": list(self.known_theorems),
            "known_conjectures": list(self.known_conjectures),
            "known_counterexamples": list(self.known_counterexamples),
            "known_computational_results": list(self.known_computational_results),
            "known_methods": list(self.known_methods),
            "known_barriers": list(self.known_barriers),
            "open_question": self.open_question,
            "open_question_confidence": self.open_question_confidence,
            "current_literature_activity": self.current_literature_activity,
            "last_checked": self.last_checked,
            "literature_ids": list(self.literature_ids),
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> PriorArtDossier:
        def _words(name: str) -> tuple[str, ...]:
            return tuple(str(item) for item in (data.get(name) or ()))

        return cls(
            target=str(data["target"]),
            definition=str(data.get("definition") or ""),
            known_equivalent_formulations=_words("known_equivalent_formulations"),
            known_theorems=_words("known_theorems"),
            known_conjectures=_words("known_conjectures"),
            known_counterexamples=_words("known_counterexamples"),
            known_computational_results=_words("known_computational_results"),
            known_methods=_words("known_methods"),
            known_barriers=_words("known_barriers"),
            open_question=str(data.get("open_question") or ""),
            open_question_confidence=str(data.get("open_question_confidence") or ""),
            current_literature_activity=str(data.get("current_literature_activity") or ""),
            last_checked=str(data.get("last_checked") or "2026-08-25"),
            literature_ids=_words("literature_ids"),
        )


@dataclass(frozen=True)
class NamedFailureCluster:
    """Semantic overlay on auto-clustered FailureRecord groups."""

    id: str
    title: str
    member_cluster_ids: tuple[str, ...]
    targets: tuple[str, ...]
    recurrence_count: int
    target_diversity: int
    mathematical_importance: ImportanceLevel
    existing_workarounds: tuple[str, ...]
    current_decision: ClusterDecision
    possible_generic_abstraction: str = ""
    research_questions: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "member_cluster_ids": list(self.member_cluster_ids),
            "targets": list(self.targets),
            "recurrence_count": self.recurrence_count,
            "target_diversity": self.target_diversity,
            "mathematical_importance": self.mathematical_importance.value,
            "existing_workarounds": list(self.existing_workarounds),
            "current_decision": self.current_decision.value,
            "possible_generic_abstraction": self.possible_generic_abstraction,
            "research_questions": list(self.research_questions),
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> NamedFailureCluster:
        return cls(
            id=str(data["id"]),
            title=str(data.get("title") or data["id"]),
            member_cluster_ids=tuple(str(item) for item in (data.get("member_cluster_ids") or ())),
            targets=tuple(str(item) for item in (data.get("targets") or ())),
            recurrence_count=int(data.get("recurrence_count") or 0),
            target_diversity=int(data.get("target_diversity") or 0),
            mathematical_importance=ImportanceLevel(
                data.get("mathematical_importance") or ImportanceLevel.MEDIUM.value
            ),
            existing_workarounds=tuple(str(item) for item in (data.get("existing_workarounds") or ())),
            current_decision=ClusterDecision(data.get("current_decision") or ClusterDecision.RECORD.value),
            possible_generic_abstraction=str(data.get("possible_generic_abstraction") or ""),
            research_questions=tuple(str(item) for item in (data.get("research_questions") or ())),
        )


@dataclass(frozen=True)
class ResearchTarget:
    """Board record. Structure is in the fields, not the name."""

    name: str
    canonical_definition: str
    state_space: str
    transition_type: str
    dimension: int
    determinism: str
    known_control_type: str
    known_regime_if_any: str
    open_question: str
    known_results: tuple[str, ...]
    known_obstructions: tuple[str, ...]
    computational_status: str
    prior_art_saturation: str
    engine_fit: ScoredAxis
    structural_distance: ScoredAxis
    novelty_potential: ScoredAxis
    failure_learning_value: ScoredAxis
    experimental_cost: ScoredAxis
    expected_research_value: ScoredAxis
    pool: TargetPool
    priority: str
    recommended_protocol: str
    claimed_capabilities: tuple[str, ...] = ()
    exact_semantics: bool = True
    finite_horizon_tractable: bool = True
    lean_certifiable: bool = True
    prior_art_classified: bool = False
    prospective_fingerprint: Any = None
    prior_art: PriorArtDossier | None = None
    blind_packet: BlindPacket | None = None
    already_run: bool = False

    def as_sketch(self):
        from research_engine.diagnosis.types import CandidateSketch

        return CandidateSketch(
            name=self.name,
            fingerprint=self.prospective_fingerprint,
            exact_semantics=self.exact_semantics,
            finite_horizon_tractable=self.finite_horizon_tractable,
            lean_certifiable=self.lean_certifiable,
            prior_art_classified=self.prior_art_classified,
            experimental_cost=self.experimental_cost.value if self.experimental_cost.value > 0 else 1.0,
            claimed_capabilities=self.claimed_capabilities,
        )

    def with_expected_value(self, value: float, reason: str) -> ResearchTarget:
        return replace(self, expected_research_value=ScoredAxis(value=value, reason=reason))

    def as_dict(self) -> dict[str, Any]:
        fingerprint = None
        if self.prospective_fingerprint is not None:
            fingerprint = self.prospective_fingerprint.as_dict()
        return {
            "name": self.name,
            "canonical_definition": self.canonical_definition,
            "state_space": self.state_space,
            "transition_type": self.transition_type,
            "dimension": self.dimension,
            "determinism": self.determinism,
            "known_control_type": self.known_control_type,
            "known_regime_if_any": self.known_regime_if_any,
            "open_question": self.open_question,
            "known_results": list(self.known_results),
            "known_obstructions": list(self.known_obstructions),
            "computational_status": self.computational_status,
            "prior_art_saturation": self.prior_art_saturation,
            "engine_fit": self.engine_fit.as_dict(),
            "structural_distance": self.structural_distance.as_dict(),
            "novelty_potential": self.novelty_potential.as_dict(),
            "failure_learning_value": self.failure_learning_value.as_dict(),
            "experimental_cost": self.experimental_cost.as_dict(),
            "expected_research_value": self.expected_research_value.as_dict(),
            "pool": self.pool.value,
            "priority": self.priority,
            "recommended_protocol": self.recommended_protocol,
            "claimed_capabilities": list(self.claimed_capabilities),
            "exact_semantics": self.exact_semantics,
            "finite_horizon_tractable": self.finite_horizon_tractable,
            "lean_certifiable": self.lean_certifiable,
            "prior_art_classified": self.prior_art_classified,
            "prospective_fingerprint": fingerprint,
            "prior_art": None if self.prior_art is None else self.prior_art.as_dict(),
            "blind_packet": None if self.blind_packet is None else self.blind_packet.as_dict(),
            "already_run": self.already_run,
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> ResearchTarget:
        raw_fp = data.get("prospective_fingerprint")
        raw_prior = data.get("prior_art")
        raw_blind = data.get("blind_packet")
        return cls(
            name=str(data["name"]),
            canonical_definition=str(data.get("canonical_definition") or ""),
            state_space=str(data.get("state_space") or ""),
            transition_type=str(data.get("transition_type") or ""),
            dimension=int(data.get("dimension") or 1),
            determinism=str(data.get("determinism") or "DETERMINISTIC"),
            known_control_type=str(data.get("known_control_type") or ""),
            known_regime_if_any=str(data.get("known_regime_if_any") or ""),
            open_question=str(data.get("open_question") or ""),
            known_results=tuple(str(item) for item in (data.get("known_results") or ())),
            known_obstructions=tuple(str(item) for item in (data.get("known_obstructions") or ())),
            computational_status=str(data.get("computational_status") or ""),
            prior_art_saturation=str(data.get("prior_art_saturation") or ""),
            engine_fit=ScoredAxis.from_dict(data.get("engine_fit") or {}),
            structural_distance=ScoredAxis.from_dict(data.get("structural_distance") or {}),
            novelty_potential=ScoredAxis.from_dict(data.get("novelty_potential") or {}),
            failure_learning_value=ScoredAxis.from_dict(data.get("failure_learning_value") or {}),
            experimental_cost=ScoredAxis.from_dict(data.get("experimental_cost") or {"value": 1.0}),
            expected_research_value=ScoredAxis.from_dict(data.get("expected_research_value") or {}),
            pool=TargetPool(data.get("pool") or TargetPool.FRONTIER.value),
            priority=str(data.get("priority") or ""),
            recommended_protocol=str(data.get("recommended_protocol") or ""),
            claimed_capabilities=tuple(str(item) for item in (data.get("claimed_capabilities") or ())),
            exact_semantics=bool(data.get("exact_semantics", True)),
            finite_horizon_tractable=bool(data.get("finite_horizon_tractable", True)),
            lean_certifiable=bool(data.get("lean_certifiable", True)),
            prior_art_classified=bool(data.get("prior_art_classified")),
            prospective_fingerprint=None if not raw_fp else fingerprint_from_dict(raw_fp),
            prior_art=None if not raw_prior else PriorArtDossier.from_dict(raw_prior),
            blind_packet=None if not raw_blind else BlindPacket.from_dict(raw_blind),
            already_run=bool(data.get("already_run")),
        )


@dataclass(frozen=True)
class CampaignOrder:
    calibration: tuple[str, ...]
    frontier: tuple[str, ...]
    wildcards: tuple[str, ...]
    research_loop_pick: str
    explanations: tuple[str, ...] = ()

    def sequence(self) -> tuple[str, ...]:
        pick = (self.research_loop_pick,) if self.research_loop_pick else ()
        return self.calibration + self.frontier + self.wildcards + pick

    def as_dict(self) -> dict[str, Any]:
        return {
            "calibration": list(self.calibration),
            "frontier": list(self.frontier),
            "wildcards": list(self.wildcards),
            "research_loop_pick": self.research_loop_pick,
            "sequence": list(self.sequence()),
            "explanations": list(self.explanations),
        }


@dataclass(frozen=True)
class TargetBoard:
    targets: tuple[ResearchTarget, ...]
    named_clusters: tuple[NamedFailureCluster, ...] = ()
    engineering_candidates: tuple[EngineeringCandidate, ...] = ()
    campaign_order: CampaignOrder | None = None

    def by_name(self) -> dict[str, ResearchTarget]:
        return {item.name: item for item in self.targets}

    def as_dict(self) -> dict[str, Any]:
        return {
            "engine_version": ENGINE_MEMORY_VERSION,
            "targets": [item.as_dict() for item in self.targets],
            "named_clusters": [item.as_dict() for item in self.named_clusters],
            "engineering_candidates": [item.as_dict() for item in self.engineering_candidates],
            "campaign_order": None if self.campaign_order is None else self.campaign_order.as_dict(),
        }

    @classmethod
    def from_dict(cls, data: MappingLike) -> TargetBoard:
        order_raw = data.get("campaign_order")
        order = None
        if order_raw:
            order = CampaignOrder(
                calibration=tuple(str(item) for item in (order_raw.get("calibration") or ())),
                frontier=tuple(str(item) for item in (order_raw.get("frontier") or ())),
                wildcards=tuple(str(item) for item in (order_raw.get("wildcards") or ())),
                research_loop_pick=str(order_raw.get("research_loop_pick") or ""),
                explanations=tuple(str(item) for item in (order_raw.get("explanations") or ())),
            )
        return cls(
            targets=tuple(ResearchTarget.from_dict(item) for item in (data.get("targets") or ())),
            named_clusters=tuple(
                NamedFailureCluster.from_dict(item) for item in (data.get("named_clusters") or ())
            ),
            engineering_candidates=tuple(
                EngineeringCandidate(
                    failure_cluster=str(item["failure_cluster"]),
                    recurrence_count=int(item.get("recurrence_count") or 0),
                    target_diversity=int(item.get("target_diversity") or 0),
                    mathematical_importance=ImportanceLevel(
                        item.get("mathematical_importance") or ImportanceLevel.MEDIUM.value
                    ),
                    expected_research_value=ImportanceLevel(
                        item.get("expected_research_value") or ImportanceLevel.MEDIUM.value
                    ),
                    implementation_cost=str(item.get("implementation_cost") or ""),
                    reusable_scope=str(item.get("reusable_scope") or ""),
                    recommendation=EngineeringRecommendation(
                        item.get("recommendation") or EngineeringRecommendation.PARK.value
                    ),
                    generic_abstraction=bool(item.get("generic_abstraction")),
                    possible_generic_abstraction=str(item.get("possible_generic_abstraction") or ""),
                    implementation_cost_estimate=str(item.get("implementation_cost_estimate") or ""),
                    current_decision=(
                        None
                        if not item.get("current_decision")
                        else EngineeringRecommendation(item["current_decision"])
                    ),
                    reason_not_implemented=str(item.get("reason_not_implemented") or ""),
                )
                for item in (data.get("engineering_candidates") or ())
            ),
            campaign_order=order,
        )


MappingLike = dict[str, Any]


def fingerprint_from_dict(data: MappingLike) -> RegimeFingerprint:
    allowed = {item.name for item in RegimeFingerprint.__dataclass_fields__.values()}
    payload = {key: str(value) for key, value in data.items() if key in allowed}
    return RegimeFingerprint(**payload)


def coverage_from_dict(data: MappingLike) -> CapabilityCoverage:
    statuses = data.get("statuses") if "statuses" in data else data
    return CapabilityCoverage(statuses={str(key): str(value) for key, value in dict(statuses).items()})


def experiment_record_to_dict(record: ExperimentRecord) -> dict[str, Any]:
    delta = None
    if record.structural_delta is not None:
        delta = {
            "level": record.structural_delta.level.value,
            "differing_dimensions": [list(item) for item in record.structural_delta.differing_dimensions],
            "similarity": {
                "score": record.structural_delta.similarity.score,
                "compared_dimensions": list(record.structural_delta.similarity.compared_dimensions),
                "matching_dimensions": list(record.structural_delta.similarity.matching_dimensions),
            },
        }
    return {
        "target": record.target,
        "semantic_class": record.semantic_class,
        "fingerprint": record.fingerprint.as_dict(),
        "family_status": record.family_status.value,
        "family_id": record.family_id,
        "nearest_target": record.nearest_target,
        "structural_delta": delta,
        "coverage": {"statuses": dict(record.coverage.statuses)},
        "strongest_exact": record.strongest_exact,
        "strongest_falsification": record.strongest_falsification,
        "lean_certificate": record.lean_certificate,
        "prior_art_status": record.prior_art_status,
        "reusable_machinery": record.reusable_machinery,
        "decision": record.decision.value,
        "decision_reason": record.decision_reason,
        "extra": dict(record.extra or {}),
    }


def experiment_record_from_dict(data: MappingLike) -> ExperimentRecord:
    from research_engine.diagnosis.types import DeltaLevel, RegimeSimilarity

    raw_delta = data.get("structural_delta")
    delta = None
    if raw_delta:
        sim = raw_delta.get("similarity") or {}
        delta = StructuralDelta(
            level=DeltaLevel(raw_delta["level"]),
            differing_dimensions=tuple(
                (str(a), str(b), str(c)) for a, b, c in (raw_delta.get("differing_dimensions") or ())
            ),
            similarity=RegimeSimilarity(
                score=float(sim.get("score") or 0.0),
                compared_dimensions=tuple(str(item) for item in (sim.get("compared_dimensions") or ())),
                matching_dimensions=tuple(str(item) for item in (sim.get("matching_dimensions") or ())),
            ),
        )
    return ExperimentRecord(
        target=str(data["target"]),
        semantic_class=str(data.get("semantic_class") or ""),
        fingerprint=fingerprint_from_dict(data.get("fingerprint") or {}),
        family_status=FamilyStatus(data.get("family_status") or FamilyStatus.ACTIVE.value),
        family_id=str(data.get("family_id") or ""),
        nearest_target=str(data.get("nearest_target") or ""),
        structural_delta=delta,
        coverage=coverage_from_dict(data.get("coverage") or {}),
        strongest_exact=str(data.get("strongest_exact") or ""),
        strongest_falsification=str(data.get("strongest_falsification") or ""),
        lean_certificate=str(data.get("lean_certificate") or ""),
        prior_art_status=str(data.get("prior_art_status") or ""),
        reusable_machinery=str(data.get("reusable_machinery") or ""),
        decision=ResearchDecision(data.get("decision") or ResearchDecision.CLOSE.value),
        decision_reason=str(data.get("decision_reason") or ""),
        extra=dict(data.get("extra") or {}) or None,
    )


__all__ = [
    "ENGINE_MEMORY_VERSION",
    "BlindPacket",
    "CampaignOrder",
    "ClusterDecision",
    "DecisionReason",
    "EngineeringBacklogItem",
    "EngineeringCandidate",
    "EngineeringRecommendation",
    "FAILURE_CLASS_DEFINITIONS",
    "FailureClass",
    "FailureCluster",
    "FailureRecord",
    "FailureStatus",
    "GreyLoot",
    "GreyLootKind",
    "GreyLootStatus",
    "ImportanceLevel",
    "KnownEquivalent",
    "LootEvidence",
    "MathematicalYield",
    "MemoryExperiment",
    "MemoryLane",
    "NamedFailureCluster",
    "NoveltyLevel",
    "NoveltyStatus",
    "PriorArtDossier",
    "PriorArtMemory",
    "Reconciliation",
    "ResearchQuestion",
    "ResearchTarget",
    "RunArtifact",
    "ScoredAxis",
    "ScoutDossier",
    "TargetBoard",
    "TargetPool",
    "coverage_from_dict",
    "experiment_record_from_dict",
    "experiment_record_to_dict",
    "fingerprint_from_dict",
]
