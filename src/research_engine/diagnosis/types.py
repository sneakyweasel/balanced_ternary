"""Evidence-gated diagnosis types. Values are never inferred from a target name."""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Any


UNOBSERVED = "UNOBSERVED"

CORE_DIMENSIONS: tuple[str, ...] = (
    "state_space_type",
    "control_structure",
    "numerical_contraction",
    "eventual_region",
    "orbit_behavior",
    "certificate_strength",
)

FINGERPRINT_DIMENSIONS: tuple[str, ...] = CORE_DIMENSIONS + (
    "transition_architecture",
    "structural_compression",
    "recurrence",
    "quotient",
    "separation",
    "symmetry",
    "block_structure",
    "reverse_structure",
    "modular_structure",
    "spectral_structure",
    "factorization_structure",
    "piecewise_affine_structure",
    "latent_control",
    "parameter_domain",
)

CAPABILITIES: tuple[str, ...] = (
    "recursive_semantics",
    "finite_closure",
    "numerical_contraction",
    "non_numerical_compression",
    "branching_controls",
    "nontrivial_control_alphabet",
    "growth",
    "valuation_dynamics",
    "modular_restrictions",
    "cycle_obstruction",
    "infinite_reachable_trajectories",
    "behavioral_quotient",
    "separation",
    "symmetry",
    "block_dynamics",
    "reverse_preimage_structure",
    "symbolic_control",
    "latent_piecewise_affine_control",
    "parameter_domain_certification",
)


class FamilyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SATURATING = "SATURATING"
    SATURATED = "SATURATED"
    CONTRADICTORY = "CONTRADICTORY"
    EXHAUSTED = "EXHAUSTED"


class ResearchDecision(str, Enum):
    CLOSE = "CLOSE"
    CONTINUE = "CONTINUE"
    ESCALATE = "ESCALATE"
    FAMILY_SATURATED = "FAMILY_SATURATED"
    ENGINE_LIMITATION = "ENGINE_LIMITATION"


class CoverageStatus(str, Enum):
    EXERCISED = "EXERCISED"
    NOT_TESTED = "NOT_TESTED"
    INAPPLICABLE = "INAPPLICABLE"


class DeltaLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class RegimeFingerprint:
    """Structural summary. Unobserved fields stay ``UNOBSERVED``."""

    transition_architecture: str = UNOBSERVED
    state_space_type: str = UNOBSERVED
    control_structure: str = UNOBSERVED
    numerical_contraction: str = UNOBSERVED
    structural_compression: str = UNOBSERVED
    eventual_region: str = UNOBSERVED
    orbit_behavior: str = UNOBSERVED
    recurrence: str = UNOBSERVED
    quotient: str = UNOBSERVED
    separation: str = UNOBSERVED
    symmetry: str = UNOBSERVED
    block_structure: str = UNOBSERVED
    reverse_structure: str = UNOBSERVED
    modular_structure: str = UNOBSERVED
    spectral_structure: str = UNOBSERVED
    factorization_structure: str = UNOBSERVED
    piecewise_affine_structure: str = UNOBSERVED
    latent_control: str = UNOBSERVED
    parameter_domain: str = UNOBSERVED
    certificate_strength: str = UNOBSERVED

    def as_dict(self) -> dict[str, str]:
        return {item.name: getattr(self, item.name) for item in fields(self)}

    def populated(self) -> dict[str, str]:
        return {key: value for key, value in self.as_dict().items() if value != UNOBSERVED}

    def core_key(self) -> tuple[str, ...] | None:
        values = tuple(getattr(self, name) for name in CORE_DIMENSIONS)
        if any(value == UNOBSERVED for value in values):
            return None
        return values


@dataclass(frozen=True)
class RegimeSimilarity:
    score: float
    compared_dimensions: tuple[str, ...]
    matching_dimensions: tuple[str, ...]


@dataclass(frozen=True)
class StructuralDelta:
    level: DeltaLevel
    differing_dimensions: tuple[tuple[str, str, str], ...]
    similarity: RegimeSimilarity


@dataclass(frozen=True)
class CapabilityCoverage:
    statuses: dict[str, str]

    def status(self, name: str) -> str:
        return self.statuses.get(name, CoverageStatus.NOT_TESTED.value)

    def exercised(self) -> tuple[str, ...]:
        return tuple(
            name
            for name in CAPABILITIES
            if self.status(name) == CoverageStatus.EXERCISED.value
        )

    def untested(self) -> tuple[str, ...]:
        return tuple(
            name
            for name in CAPABILITIES
            if self.status(name) == CoverageStatus.NOT_TESTED.value
        )


@dataclass(frozen=True)
class ExperimentRecord:
    target: str
    semantic_class: str
    fingerprint: RegimeFingerprint
    family_status: FamilyStatus
    family_id: str
    nearest_target: str
    structural_delta: StructuralDelta | None
    coverage: CapabilityCoverage
    strongest_exact: str
    strongest_falsification: str
    lean_certificate: str
    prior_art_status: str
    reusable_machinery: str
    decision: ResearchDecision
    decision_reason: str
    extra: dict[str, Any] | None = None


@dataclass(frozen=True)
class CandidateSketch:
    name: str
    fingerprint: RegimeFingerprint | None = None
    exact_semantics: bool = True
    finite_horizon_tractable: bool = True
    lean_certifiable: bool = True
    prior_art_classified: bool = False
    experimental_cost: float = 1.0
    claimed_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class SelectionReport:
    name: str
    value: float
    structural_distance: float
    capability_gap: float
    novelty_potential: float
    experimental_cost: float
    explanation: str
