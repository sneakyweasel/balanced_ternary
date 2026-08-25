"""Link Syracuse certificates to Lean names. Does not generate proofs."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

SYRACUSE_MODULE = "Problems.Collatz.Syracuse"
ONE_THEOREM = "syracuseS_one"
ODD_THEOREM = "acceleratedT_odd"


def closure_is_inconclusive(report: PlannerReport) -> bool:
    closure = next((item for item in report.results if item.name == "closure"), None)
    return (
        closure is not None
        and closure.status is AttackStatus.INCONCLUSIVE
        and closure.scope is SearchScope.BOUNDED
        and closure.kind is ClaimKind.REACHABLE
    )


def export_syracuse_targets(report: PlannerReport) -> tuple[TheoremTarget, ...]:
    targets = targets_from_report(report, problem="syracuse")
    fixed = TheoremTarget(
        name="syracuse_one_fixed",
        statement="S(1)=1 on the positive odd integers",
        kind=ClaimKind.REACHABLE,
        scope=SearchScope.EXACT,
        exportable=True,
        reason="exact supported identity",
        attack="closure",
        problem="syracuse",
        finite_checks=("S(1)=1",),
    )
    linked = attach_lean(
        fixed,
        module=SYRACUSE_MODULE,
        theorem=ONE_THEOREM,
        name="syracuse_one_fixed",
    )
    out: list[TheoremTarget] = [linked]
    for item in targets:
        if item.attack == "parameter_domain" and item.exportable:
            out.append(
                attach_lean(
                    item,
                    module="Problems.Collatz.Syracuse",
                    theorem="syracuseS_parameter_iff",
                )
            )
        else:
            out.append(item)
    return tuple(out)
