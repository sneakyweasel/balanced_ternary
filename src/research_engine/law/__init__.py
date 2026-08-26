"""Affine-law discovery independent of region partition. Research Engine v2.3 Phase 3."""

from research_engine.law.analyze import analyze, hypotheses_from_report
from research_engine.law.discipline import (
    live_hypothesis_unpromoted,
    truncated_domain_is_not_certified,
    unresolved_census_stays_unresolved,
)
from research_engine.law.extract import extract_pairs
from research_engine.law.types import (
    ENGINE_LAW_VERSION,
    AffineLaw,
    DomainAttachment,
    DomainEvidence,
    LawDomainPair,
    LawDomainReport,
    LawEvidence,
)

__all__ = [
    "ENGINE_LAW_VERSION",
    "AffineLaw",
    "DomainAttachment",
    "DomainEvidence",
    "LawDomainPair",
    "LawDomainReport",
    "LawEvidence",
    "analyze",
    "extract_pairs",
    "hypotheses_from_report",
    "live_hypothesis_unpromoted",
    "truncated_domain_is_not_certified",
    "unresolved_census_stays_unresolved",
]
