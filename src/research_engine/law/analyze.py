"""Top-level law/domain entry. Opt-in; not a flood-order attack."""

from __future__ import annotations

from dataclasses import replace

from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.law.discipline import truncated_domain_is_not_certified
from research_engine.law.extract import extract_pairs, flood_census_kind
from research_engine.law.types import (
    ENGINE_LAW_VERSION,
    DomainEvidence,
    LawDomainReport,
    LawEvidence,
)
from research_engine.memory.types import NoveltyStatus
from research_engine.strategy.types import (
    ObligationKind,
    ProofObligation,
    ResearchHypothesis,
    ResearchHypothesisStatus,
)

_KNOWN = {
    "slc_negation": "affine involution y = -x (domain may be sign-truncated)",
    "slc_decrement": "affine decrement y = x-1 on the nonnegative sample class",
}


def _novelty(name: str) -> tuple[NoveltyStatus, str]:
    known = _KNOWN.get(name, "")
    if known:
        return NoveltyStatus.KNOWN_REDISCOVERY, known
    return NoveltyStatus.UNKNOWN, ""


def analyze(spec: ProblemSpec, context: AttackContext | None = None) -> LawDomainReport:
    if context is not None:
        ctx = context
    else:
        maker = getattr(spec, "attack_context", None)
        ctx = maker() if callable(maker) else AttackContext()
    target = str(getattr(spec, "name", "") or "")
    novelty, _closest = _novelty(target)
    pairs = []
    for item in extract_pairs(spec, ctx):
        law = replace(item.law, novelty_status=novelty, source_target=target)
        domain = replace(item.domain, source_target=target)
        pairs.append(replace(item, law=law, domain=domain))
    report = LawDomainReport(
        source_target=target,
        census_kind=flood_census_kind(spec, ctx),
        pairs=tuple(pairs),
        version=ENGINE_LAW_VERSION,
    )
    if not truncated_domain_is_not_certified(report):
        repaired = []
        for item in report.pairs:
            if item.domain.truncated and item.domain.evidence is DomainEvidence.DOMAIN_CERTIFIED:
                item = replace(
                    item,
                    domain=replace(
                        item.domain,
                        evidence=DomainEvidence.DOMAIN_TRUNCATED,
                        statement="truncated region cannot be DOMAIN_CERTIFIED",
                    ),
                )
            repaired.append(item)
        report = replace(report, pairs=tuple(repaired))
    return report


def hypotheses_from_report(report: LawDomainReport) -> tuple[ResearchHypothesis, ...]:
    items: list[ResearchHypothesis] = []
    closest = _KNOWN.get(report.source_target, "")
    novelty, _ = _novelty(report.source_target)
    for index, pair in enumerate(report.pairs):
        law = pair.law
        domain = pair.domain
        if law.evidence is LawEvidence.LAW_CERTIFIED:
            status = ResearchHypothesisStatus.PROOF_READY
        elif law.evidence is LawEvidence.LAW_CANDIDATE:
            status = ResearchHypothesisStatus.SEARCH_SUPPORTED
        else:
            continue
        obligations = [
            ProofObligation(kind=ObligationKind.LAW_CERTIFICATION, statement="Need: affine law q y = p x + r"),
        ]
        if domain.evidence is not DomainEvidence.DOMAIN_CERTIFIED:
            obligations.append(
                ProofObligation(
                    kind=ObligationKind.DOMAIN_CERTIFICATION,
                    statement="Need: exact domain D_u",
                    status="OPEN",
                )
            )
        items.append(
            ResearchHypothesis(
                id=f"hyp:{report.source_target}:law:{index}",
                statement=law.statement or "affine law",
                target=report.source_target,
                source_target=report.source_target,
                evidence=law.evidence.value,
                supporting_artifacts=("law.affine", f"census_kind:{report.census_kind}"),
                counterexamples=tuple(str(item) for item in law.counterexamples),
                confidence=0.8 if status is ResearchHypothesisStatus.PROOF_READY else 0.45,
                current_status=status,
                closest_known_result=closest,
                prior_art_matches=(closest,) if closest else (),
                proof_obligations=tuple(obligations),
                novelty_status=novelty,
                kind=ClaimKind.REACHABLE,
                intended_scope=SearchScope.BOUNDED,
                cluster_id="census_domain" if domain.truncated else "",
            )
        )
    return tuple(items)
