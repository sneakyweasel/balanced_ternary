"""Top-level global-reasoning entry. Opt-in; not a flood-order attack."""

from __future__ import annotations

from dataclasses import replace

from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.memory.types import NoveltyStatus
from research_engine.reasoning.cegis import synthesize_invariant
from research_engine.reasoning.discipline import finalize_invariant, finalize_ranking, from_closure
from research_engine.reasoning.ranking import synthesize_ranking
from research_engine.reasoning.types import (
    ENGINE_REASONING_VERSION,
    EvidenceState,
    ReasoningReport,
)
from research_engine.strategy.types import (
    ObligationKind,
    ProofObligation,
    ResearchHypothesis,
    ResearchHypothesisStatus,
)

_KNOWN = {
    "two_path_z2": "N^2 invariance / origin-avoidance on the two-path map",
    "slc_decrement": "strict decrement ranking on positive integers",
    "euclidean_quotient": "Euclidean remainder ranking",
}


def _novelty(name: str) -> tuple[NoveltyStatus, str]:
    known = _KNOWN.get(name, "")
    if known:
        return NoveltyStatus.KNOWN_REDISCOVERY, known
    return NoveltyStatus.UNKNOWN, ""


def analyze(spec: ProblemSpec, context: AttackContext | None = None) -> ReasoningReport:
    if context is not None:
        ctx = context
    else:
        maker = getattr(spec, "attack_context", None)
        ctx = maker() if callable(maker) else AttackContext()
    target = str(getattr(spec, "name", "") or "")
    novelty, _closest = _novelty(target)
    invariant, observed, complete = synthesize_invariant(spec, ctx)
    if invariant is not None:
        invariant = replace(
            finalize_invariant(invariant),
            novelty_status=novelty,
            source_target=target,
        )
    ranking = synthesize_ranking(spec, ctx, invariant)
    if ranking is not None:
        ranking = replace(
            finalize_ranking(ranking),
            novelty_status=novelty,
            source_target=target,
        )
    return ReasoningReport(
        source_target=target,
        observed=observed,
        closure_complete=complete,
        invariant=invariant,
        ranking=ranking,
        version=ENGINE_REASONING_VERSION,
    )


def hypotheses_from_report(report: ReasoningReport) -> tuple[ResearchHypothesis, ...]:
    items: list[ResearchHypothesis] = []
    closest = _KNOWN.get(report.source_target, "")
    novelty, _ = _novelty(report.source_target)
    if report.invariant is not None:
        cert = report.invariant
        status = ResearchHypothesisStatus.CANDIDATE
        if cert.evidence is EvidenceState.INDUCTIVE_CERTIFIED:
            status = ResearchHypothesisStatus.PROOF_READY
        elif cert.evidence is EvidenceState.INDUCTIVE_CANDIDATE:
            status = ResearchHypothesisStatus.SEARCH_SUPPORTED
        elif cert.evidence is EvidenceState.FINITE_EXACT:
            status = ResearchHypothesisStatus.SEARCH_SUPPORTED
        items.append(
            ResearchHypothesis(
                id=f"hyp:{report.source_target}:inductive",
                statement=cert.statement or "T(S) ⊆ S",
                target=report.source_target,
                source_target=report.source_target,
                evidence=cert.evidence.value,
                supporting_artifacts=("reasoning.invariant",),
                counterexamples=cert.counterexamples,
                confidence=0.8 if status is ResearchHypothesisStatus.PROOF_READY else 0.45,
                current_status=status,
                closest_known_result=closest,
                prior_art_matches=(closest,) if closest else (),
                proof_obligations=(
                    ProofObligation(kind=ObligationKind.INDUCTIVE_INCLUSION, statement="Need: T(S) ⊆ S"),
                ),
                novelty_status=novelty,
                kind=ClaimKind.REACHABLE,
                intended_scope=SearchScope.BOUNDED,
            )
        )
    if report.ranking is not None:
        cert = report.ranking
        status = ResearchHypothesisStatus.CANDIDATE
        if cert.evidence is EvidenceState.RANKING_CERTIFIED:
            status = ResearchHypothesisStatus.PROOF_READY
        elif cert.evidence is EvidenceState.RANKING_CANDIDATE:
            status = ResearchHypothesisStatus.SEARCH_SUPPORTED
        items.append(
            ResearchHypothesis(
                id=f"hyp:{report.source_target}:ranking",
                statement=cert.statement or "V(T(x)) < V(x)",
                target=report.source_target,
                source_target=report.source_target,
                evidence=cert.evidence.value,
                supporting_artifacts=("reasoning.ranking",),
                counterexamples=cert.counterexamples,
                confidence=0.8 if status is ResearchHypothesisStatus.PROOF_READY else 0.45,
                current_status=status,
                closest_known_result=closest,
                prior_art_matches=(closest,) if closest else (),
                proof_obligations=(
                    ProofObligation(kind=ObligationKind.RANKING_DESCENT, statement="Need: V(T(x)) < V(x)"),
                ),
                novelty_status=novelty,
                kind=ClaimKind.REACHABLE,
                intended_scope=SearchScope.BOUNDED,
            )
        )
    if report.closure_complete and report.invariant is None:
        items.append(
            ResearchHypothesis(
                id=f"hyp:{report.source_target}:finite_exact",
                statement="exact residual closure is finite at the frozen initial phase",
                target=report.source_target,
                source_target=report.source_target,
                evidence=from_closure(complete=True).value,
                supporting_artifacts=("reasoning.closure",),
                current_status=ResearchHypothesisStatus.SEARCH_SUPPORTED,
                closest_known_result=closest,
                novelty_status=novelty,
                kind=ClaimKind.REACHABLE,
                intended_scope=SearchScope.EXACT,
            )
        )
    return tuple(items)
