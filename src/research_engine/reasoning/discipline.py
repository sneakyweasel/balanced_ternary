"""Finite-to-infinite evidence rules. Finite closure is never UNIVERSAL_THEOREM."""

from __future__ import annotations

from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.reasoning.types import EvidenceState, InvariantCertificate, RankingCertificate
from research_engine.core.semantics import ClaimKind, SearchScope


_CERTIFIED = {
    EvidenceState.INDUCTIVE_CERTIFIED,
    EvidenceState.RANKING_CERTIFIED,
}


def from_closure(*, complete: bool) -> EvidenceState:
    return EvidenceState.FINITE_EXACT if complete else EvidenceState.FINITE_OBSERVATION


def clamp_universal(state: EvidenceState, *, universal_domain: bool) -> EvidenceState:
    if state is EvidenceState.UNIVERSAL_THEOREM and not universal_domain:
        return EvidenceState.UNKNOWN
    return state


def finalize_invariant(certificate: InvariantCertificate) -> InvariantCertificate:
    from dataclasses import replace

    if certificate.universal_domain and certificate.evidence in _CERTIFIED:
        return replace(certificate, evidence=EvidenceState.UNIVERSAL_THEOREM)
    evidence = certificate.evidence
    if evidence is EvidenceState.UNIVERSAL_THEOREM:
        evidence = EvidenceState.INDUCTIVE_CERTIFIED
    return replace(certificate, evidence=clamp_universal(evidence, universal_domain=False))


def finalize_ranking(certificate: RankingCertificate) -> RankingCertificate:
    from dataclasses import replace

    if certificate.evidence is EvidenceState.UNIVERSAL_THEOREM:
        return replace(certificate, evidence=EvidenceState.RANKING_CERTIFIED)
    return certificate


def live_hypothesis_unpromoted(hyp: Hypothesis) -> bool:
    """Session LIVE hypotheses stay OPEN under finite/inductive evidence."""

    return hyp.kind is ClaimKind.LIVE and hyp.status is HypothesisStatus.OPEN


def finite_exact_is_not_universal(state: EvidenceState) -> bool:
    return state is not EvidenceState.UNIVERSAL_THEOREM


def exact_scope_required_for_live(scope: SearchScope) -> bool:
    return scope is SearchScope.EXACT
