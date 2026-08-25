"""Link signed-digit residual certificates to Lean names. Does not generate proofs."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

SDR_MODULE = "Problems.BalancedTernary.SignedDigitResidual"
CLOSURE_THEOREM = "lambda1_u2_residual_closure"
FINITE_THEOREM = "finite_residual_condition"
UNBOUNDED_THEOREM = "gain3_control2_unbounded"


def closure_is_exact_size(report: PlannerReport, size: int) -> bool:
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is None:
        return False
    if closure.status is not AttackStatus.SUPPORTED:
        return False
    if closure.scope is not SearchScope.EXACT:
        return False
    if closure.kind is not ClaimKind.REACHABLE:
        return False
    return closure.evidence.get("union_size") == size and closure.evidence.get("complete") is True


def link_signed_digit_targets(
    targets: tuple[TheoremTarget, ...],
) -> tuple[TheoremTarget, ...]:
    out: list[TheoremTarget] = []
    for target in targets:
        if (
            target.attack == "closure"
            and target.exportable
            and target.kind is ClaimKind.REACHABLE
        ):
            size = None
            for cert in target.certificates:
                if isinstance(cert, dict) and cert.get("size") == 3:
                    size = 3
            if size == 3:
                out.append(
                    attach_lean(
                        target,
                        module=SDR_MODULE,
                        theorem=CLOSURE_THEOREM,
                        name="signed_digit_u2_residual_closure",
                    )
                )
                continue
        out.append(target)
    return tuple(out)


def export_signed_digit_targets(report: PlannerReport) -> tuple[TheoremTarget, ...]:
    return link_signed_digit_targets(
        targets_from_report(report, problem="signed_digit_residual")
    )
