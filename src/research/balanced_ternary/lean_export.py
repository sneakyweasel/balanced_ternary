"""Link doubled-trit certificates to Lean names. Does not generate proofs."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

CLOSURE_MODULE = "Problems.BalancedTernary.FiniteStateDynamics"
CLOSURE_THEOREM = "doubledTrit_closure"
LYAPUNOV_THEOREM = "doubledTrit_lyapunov"
SIGN_THEOREM = "doubledTrit_sign"
GAIN3_THEOREM = "carryGain3_unbounded"


def link_balanced_ternary_targets(
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
                        module=CLOSURE_MODULE,
                        theorem=CLOSURE_THEOREM,
                        name="doubled_trit_residual_closure",
                    )
                )
                continue
        out.append(target)
    return tuple(out)


def export_plan_targets(report: PlannerReport) -> tuple[TheoremTarget, ...]:
    return link_balanced_ternary_targets(
        targets_from_report(report, problem="balanced_ternary")
    )


def closure_is_exact_three(report: PlannerReport) -> bool:
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is None:
        return False
    if closure.status is not AttackStatus.SUPPORTED:
        return False
    if closure.scope is not SearchScope.EXACT:
        return False
    if closure.kind is not ClaimKind.REACHABLE:
        return False
    return closure.evidence.get("union_size") == 3 and closure.evidence.get("complete") is True
