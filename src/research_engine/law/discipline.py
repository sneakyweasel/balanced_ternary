"""LAW_CERTIFIED is not a finite census and not a universal theorem."""

from __future__ import annotations

from research_engine.attacks.piecewise_affine import CensusKind
from research_engine.law.types import DomainEvidence, LawDomainReport, LawEvidence
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.core.semantics import ClaimKind


def truncated_domain_is_not_certified(report: LawDomainReport) -> bool:
    for pair in report.pairs:
        if pair.domain.truncated and pair.domain.evidence is DomainEvidence.DOMAIN_CERTIFIED:
            return False
        if pair.domain.evidence is DomainEvidence.DOMAIN_TRUNCATED and pair.domain.evidence is DomainEvidence.DOMAIN_CERTIFIED:
            return False
    return True


def unresolved_census_stays_unresolved(report: LawDomainReport) -> bool:
    """Certified laws do not rewrite an UNRESOLVED flood census."""

    return report.census_kind != CensusKind.FINITE_CENSUS.value or not any(
        pair.domain.truncated and pair.law.evidence is LawEvidence.LAW_CERTIFIED for pair in report.pairs
    )


def live_hypothesis_unpromoted(hyp: Hypothesis) -> bool:
    return hyp.kind is ClaimKind.LIVE and hyp.status is HypothesisStatus.OPEN
