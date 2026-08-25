"""Link short-horizon certificates to Lean names. Does not generate proofs."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

SDSH_MODULE = "Problems.BalancedTernary.SignedDigitShortHorizon"
CLOSURE_THEOREM = "truncated_3adic_equiv"


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


def link_short_horizon_targets(
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
                if isinstance(cert, dict) and cert.get("size") == 7:
                    size = 7
            if size == 7:
                out.append(
                    attach_lean(
                        target,
                        module=SDSH_MODULE,
                        theorem=CLOSURE_THEOREM,
                        name="horizon_u2_truncated_mod",
                    )
                )
                continue
        out.append(target)
    return tuple(out)


def export_short_horizon_targets(report: PlannerReport) -> tuple[TheoremTarget, ...]:
    return link_short_horizon_targets(
        targets_from_report(report, problem="signed_digit_short_horizon")
    )
