"""Link weight-drift certificates to Lean names. Does not generate proofs."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

DRIFT_MODULE = "Problems.BalancedTernary.WeightDrift"
DRIFT_THEOREM = "weightDriftZ_gt"


def closure_is_inconclusive(report: PlannerReport) -> bool:
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is None:
        return False
    return (
        closure.status is AttackStatus.INCONCLUSIVE
        and closure.scope is SearchScope.BOUNDED
        and closure.kind is ClaimKind.REACHABLE
        and closure.evidence.get("complete") is False
    )


def link_weight_drift_targets(
    targets: tuple[TheoremTarget, ...],
) -> tuple[TheoremTarget, ...]:
    extra = TheoremTarget(
        name="weight_drift_increase",
        statement="if n ≠ 0 then n < n + W(n)",
        kind=ClaimKind.REACHABLE,
        scope=SearchScope.EXACT,
        exportable=True,
        reason="exact supported certificate",
        attack="functional",
        problem="balanced_ternary_weight_drift",
    )
    extra = attach_lean(
        extra,
        module=DRIFT_MODULE,
        theorem=DRIFT_THEOREM,
        name="weight_drift_increase",
    )
    return tuple(targets) + (extra,)


def export_weight_drift_targets(report: PlannerReport) -> tuple[TheoremTarget, ...]:
    return link_weight_drift_targets(
        targets_from_report(report, problem="balanced_ternary_weight_drift")
    )
