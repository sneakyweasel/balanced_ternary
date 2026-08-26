"""v2.3 Phase 3 law/domain types. A sample law is not a finite census."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from research_engine.attacks.piecewise_affine import BranchRegion
from research_engine.memory.types import NoveltyStatus

ENGINE_LAW_VERSION = "0.2.5"

MappingLike = Mapping[str, Any]


class LawEvidence(str, Enum):
    LAW_CANDIDATE = "LAW_CANDIDATE"
    LAW_CERTIFIED = "LAW_CERTIFIED"
    LAW_REFUTED = "LAW_REFUTED"
    UNKNOWN = "UNKNOWN"


class DomainEvidence(str, Enum):
    DOMAIN_UNKNOWN = "DOMAIN_UNKNOWN"
    DOMAIN_TRUNCATED = "DOMAIN_TRUNCATED"
    DOMAIN_CANDIDATE = "DOMAIN_CANDIDATE"
    DOMAIN_CERTIFIED = "DOMAIN_CERTIFIED"


@dataclass(frozen=True)
class AffineLaw:
    """Cleared identity ``q y = p x + r``, or a parameterized family handle."""

    p: int
    q: int | None
    r: int
    support: tuple[int, ...]
    evidence: LawEvidence
    counterexamples: tuple[int, ...] = ()
    family_base: int | None = None
    observed_k: tuple[int, ...] = ()
    source_target: str = ""
    novelty_status: NoveltyStatus = NoveltyStatus.UNKNOWN
    statement: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "p": self.p,
            "q": self.q,
            "r": self.r,
            "support": list(self.support),
            "evidence": self.evidence.value,
            "counterexamples": list(self.counterexamples),
            "family_base": self.family_base,
            "observed_k": list(self.observed_k),
            "source_target": self.source_target,
            "novelty_status": self.novelty_status.value,
            "statement": self.statement,
        }


@dataclass(frozen=True)
class DomainAttachment:
    """Optional region from existing infer_region. Not a Z-cover theorem."""

    region: BranchRegion | None
    evidence: DomainEvidence
    region_points: tuple[int, ...] = ()
    truncated: bool = False
    source_target: str = ""
    statement: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "region": None if self.region is None else self.region.as_dict(),
            "evidence": self.evidence.value,
            "region_points": list(self.region_points),
            "truncated": self.truncated,
            "source_target": self.source_target,
            "statement": self.statement,
        }


@dataclass(frozen=True)
class LawDomainPair:
    law: AffineLaw
    domain: DomainAttachment

    def as_dict(self) -> dict[str, Any]:
        return {"law": self.law.as_dict(), "domain": self.domain.as_dict()}


@dataclass(frozen=True)
class LawDomainReport:
    source_target: str
    census_kind: str
    pairs: tuple[LawDomainPair, ...] = ()
    version: str = ENGINE_LAW_VERSION

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_target": self.source_target,
            "census_kind": self.census_kind,
            "pairs": [item.as_dict() for item in self.pairs],
            "version": self.version,
        }
