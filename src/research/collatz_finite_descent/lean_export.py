"""Link shortcut-Collatz certificates to Lean names. Does not generate proofs."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

SHORTCUT_MODULE = "Problems.Collatz.Shortcut"
TERMINAL_THEOREM = "shortcutC_terminal_cycle"
BLOCK_THEOREM = "shortcutC_block_odd"
DESCENT_THEOREM = "shortcutC_no_uniform_L_descent"
LYAPUNOV_THEOREM = "shortcutC_odd_increases"


def closure_is_inconclusive(report: PlannerReport) -> bool:
    closure = next((item for item in report.results if item.name == "closure"), None)
    return (
        closure is not None
        and closure.status is AttackStatus.INCONCLUSIVE
        and closure.scope is SearchScope.BOUNDED
        and closure.kind is ClaimKind.REACHABLE
    )


def link_collatz_finite_descent_targets(
    targets: tuple[TheoremTarget, ...],
) -> tuple[TheoremTarget, ...]:
    obstruction = TheoremTarget(
        name="no_uniform_L_descent",
        statement=(
            "For every L ≥ 1, n = 2^L - 1 realises the all-odd word of "
            "length L and C^L(n) > n"
        ),
        kind=ClaimKind.REACHABLE,
        scope=SearchScope.EXACT,
        exportable=True,
        reason="exact supported certificate",
        attack="block",
        problem="collatz_finite_descent",
        finite_checks=("witness=2^L-1",),
    )
    linked = attach_lean(
        obstruction,
        module=SHORTCUT_MODULE,
        theorem=DESCENT_THEOREM,
        name="no_uniform_L_descent",
    )
    return (linked,) + tuple(targets)


def export_collatz_finite_descent_targets(
    report: PlannerReport,
) -> tuple[TheoremTarget, ...]:
    return link_collatz_finite_descent_targets(
        targets_from_report(report, problem="collatz_finite_descent")
    )
