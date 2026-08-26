"""Counterexample-first checks using existing leak attacks. Not a prover."""

from __future__ import annotations

from dataclasses import replace

from research_engine.attacks.counterexample import (
    ClosureLeakAttack,
    DescentLeakAttack,
    InvariantLeakAttack,
)
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.strategy.types import (
    ObligationKind,
    ResearchHypothesis,
    ResearchHypothesisStatus,
)


def _obligation_kinds(hypothesis: ResearchHypothesis) -> set[ObligationKind]:
    return {item.kind for item in hypothesis.proof_obligations}


def _looks_inductive(hypothesis: ResearchHypothesis) -> bool:
    kinds = _obligation_kinds(hypothesis)
    if ObligationKind.INDUCTIVE_INCLUSION in kinds or ObligationKind.MATRIX_INVARIANT in kinds:
        return True
    text = hypothesis.statement.lower()
    return "invariant" in text or "t(s)" in text or "⊆" in hypothesis.statement


def _looks_ranking(hypothesis: ResearchHypothesis) -> bool:
    if ObligationKind.RANKING_DESCENT in _obligation_kinds(hypothesis):
        return True
    text = hypothesis.statement.lower()
    return "ranking" in text or "v(t" in text or "descend" in text


def falsify(
    hypothesis: ResearchHypothesis,
    spec: ProblemSpec,
    context: AttackContext | None = None,
) -> ResearchHypothesis:
    """Attempt small counterexamples before any proof-search language.

    A leak-free sample becomes ``SEARCH_SUPPORTED``. It is not a ledger theorem.
    """

    if hypothesis.current_status is ResearchHypothesisStatus.REFUTED:
        return hypothesis
    ctx = context if context is not None else AttackContext()
    attacks = []
    if _looks_inductive(hypothesis):
        attacks.append(InvariantLeakAttack())
        attacks.append(ClosureLeakAttack())
    if _looks_ranking(hypothesis):
        attacks.append(DescentLeakAttack())
    if not attacks:
        attacks.append(InvariantLeakAttack())
    for attack in attacks:
        if not attack.applicable(spec, ctx):
            continue
        result = attack.run(spec, ctx)
        if result.status is AttackStatus.REFUTED:
            witnesses = tuple(str(item) for item in result.counterexamples[:8])
            return replace(
                hypothesis,
                current_status=ResearchHypothesisStatus.REFUTED,
                counterexamples=witnesses or hypothesis.counterexamples,
                evidence=result.claim,
                confidence=0.95,
            )
        if result.status is AttackStatus.SUPPORTED:
            status = ResearchHypothesisStatus.SEARCH_SUPPORTED
            if hypothesis.current_status in {
                ResearchHypothesisStatus.PROOF_READY,
                ResearchHypothesisStatus.PROVED,
                ResearchHypothesisStatus.LEAN_CERTIFIED,
            }:
                status = hypothesis.current_status
            return replace(
                hypothesis,
                current_status=status,
                evidence=result.claim,
            )
        if result.status is AttackStatus.OBSERVATION and not result.counterexamples:
            if hypothesis.current_status is ResearchHypothesisStatus.CANDIDATE:
                return replace(
                    hypothesis,
                    current_status=ResearchHypothesisStatus.SEARCH_SUPPORTED,
                    evidence=result.claim,
                )
    return hypothesis
