"""v2.3 Phase 2 global-reasoning types. Not a theorem ledger and not a solver."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Mapping

from research_engine.core.semantics import State
from research_engine.memory.types import NoveltyStatus

ENGINE_REASONING_VERSION = "0.2.4"

MappingLike = Mapping[str, Any]


class EvidenceState(str, Enum):
    """Finite-to-infinite evidence. Finite closure is never a universal theorem."""

    FINITE_OBSERVATION = "FINITE_OBSERVATION"
    FINITE_EXACT = "FINITE_EXACT"
    INDUCTIVE_CANDIDATE = "INDUCTIVE_CANDIDATE"
    INDUCTIVE_CERTIFIED = "INDUCTIVE_CERTIFIED"
    RANKING_CANDIDATE = "RANKING_CANDIDATE"
    RANKING_CERTIFIED = "RANKING_CERTIFIED"
    UNIVERSAL_THEOREM = "UNIVERSAL_THEOREM"
    UNKNOWN = "UNKNOWN"


class RegionForm(str, Enum):
    FINITE_SET = "FINITE_SET"
    INTERVAL = "INTERVAL"
    SIGN_ORTHANT = "SIGN_ORTHANT"
    MODULAR_CLASS = "MODULAR_CLASS"


@dataclass(frozen=True)
class Region:
    """Descriptor of a state region. Membership is exact for the listed forms."""

    form: RegionForm
    parameters: Mapping[str, Any] = field(default_factory=dict)
    dimension: int = 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "form": self.form.value,
            "parameters": dict(self.parameters),
            "dimension": self.dimension,
        }


@dataclass(frozen=True)
class InvariantCertificate:
    """S0 ⊆ S and T(S) ⊆ S. Not a live-set theorem."""

    region: Region
    seeds: tuple[State, ...]
    seeds_included: bool
    transition_closed: bool
    evidence: EvidenceState
    counterexamples: tuple[str, ...] = ()
    source_target: str = ""
    probe_size: int = 0
    universal_domain: bool = False
    novelty_status: NoveltyStatus = NoveltyStatus.UNKNOWN
    statement: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "region": self.region.as_dict(),
            "seeds": [list(item) for item in self.seeds],
            "seeds_included": self.seeds_included,
            "transition_closed": self.transition_closed,
            "evidence": self.evidence.value,
            "counterexamples": list(self.counterexamples),
            "source_target": self.source_target,
            "probe_size": self.probe_size,
            "universal_domain": self.universal_domain,
            "novelty_status": self.novelty_status.value,
            "statement": self.statement,
        }


@dataclass(frozen=True)
class RankingCertificate:
    """V(T(x)) < V(x) on a region. A sample descent is not a Lyapunov theorem."""

    name: str
    evaluate: Callable[[State], int | tuple[int, ...]]
    region: Region
    evidence: EvidenceState
    counterexamples: tuple[str, ...] = ()
    source_target: str = ""
    probe_size: int = 0
    novelty_status: NoveltyStatus = NoveltyStatus.UNKNOWN
    statement: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "region": self.region.as_dict(),
            "evidence": self.evidence.value,
            "counterexamples": list(self.counterexamples),
            "source_target": self.source_target,
            "probe_size": self.probe_size,
            "novelty_status": self.novelty_status.value,
            "statement": self.statement,
        }


@dataclass(frozen=True)
class ReasoningReport:
    source_target: str
    observed: tuple[State, ...]
    closure_complete: bool
    invariant: InvariantCertificate | None = None
    ranking: RankingCertificate | None = None
    version: str = ENGINE_REASONING_VERSION

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_target": self.source_target,
            "observed": [list(item) for item in self.observed],
            "closure_complete": self.closure_complete,
            "invariant": None if self.invariant is None else self.invariant.as_dict(),
            "ranking": None if self.ranking is None else self.ranking.as_dict(),
            "version": self.version,
        }
