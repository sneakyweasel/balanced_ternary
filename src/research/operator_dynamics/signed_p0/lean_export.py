"""Link N∘I₀∘D certificates to Lean names. Does not generate proofs."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

SIGNED_P0_MODULE = "Problems.BalancedTernary.SignedP0"
CLOSURE_THEOREM = "signedP0_sq_eq_P0"


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


def link_signed_p0_targets(
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
                        module=SIGNED_P0_MODULE,
                        theorem=CLOSURE_THEOREM,
                        name="signed_p0_orbit_law",
                    )
                )
                continue
        out.append(target)
    return tuple(out)


def export_signed_p0_targets(report: PlannerReport) -> tuple[TheoremTarget, ...]:
    return link_signed_p0_targets(
        targets_from_report(report, problem="operator_dynamics_benchmark")
    )
