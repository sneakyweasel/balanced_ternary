"""Optional raw-contribution factorization as an attack."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.contribution import (
    FactorizationStatus,
    check_control_factorization,
    has_raw_contribution,
)
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope


class FactorizationAttack:
    name = "factorization"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del context
        return has_raw_contribution(spec)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not has_raw_contribution(spec):
            return inapplicable(self.name, "no raw_contribution map", ClaimKind.REACHABLE)
        region = context.candidate_region
        states = tuple(region) if region else None
        result = check_control_factorization(spec, states=states)
        if result.status is FactorizationStatus.INAPPLICABLE:
            return inapplicable(self.name, result.claim, ClaimKind.REACHABLE)
        if result.status is FactorizationStatus.REFUTED:
            return AttackResult(
                name=self.name,
                status=AttackStatus.REFUTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=result.claim,
                evidence={
                    "control_count": result.control_count,
                    "contribution_count": result.contribution_count,
                },
                counterexamples=(result.witness,) if result.witness is not None else (),
                certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.SUPPORTED,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.EXACT,
            claim=result.claim,
            evidence={
                "control_count": result.control_count,
                "contribution_count": result.contribution_count,
                "contributions": result.contributions,
            },
            certificate_kind=CertificateKind.EXACT_CLOSURE,
        )
