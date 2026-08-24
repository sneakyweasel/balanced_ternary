"""Plain-text reports of planner output. Not proofs, and not a CLI."""

from __future__ import annotations

from collections.abc import Sequence

from research_engine.attacks.result import AttackResult
from research_engine.core.semantics import ClaimKind
from research_engine.planner.hypothesis import Hypothesis
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import TheoremTarget, render_yaml

DISCLAIMER = (
    "A bounded census is not an asymptotic theorem. "
    "LIVE infinitude is not decided here."
)


def format_attack_result(result: AttackResult) -> str:
    return (
        f"attack {result.name}: {result.status.value} "
        f"{result.scope.value} {result.kind.value}\n"
        f"  {result.claim}"
    )


def format_hypothesis(hyp: Hypothesis) -> str:
    return (
        f"hypothesis {hyp.id}: {hyp.status.value} "
        f"{hyp.intended_scope.value} {hyp.kind.value}\n"
        f"  {hyp.statement}"
    )


def format_planner_report(report: PlannerReport, *, problem: str) -> str:
    lines = [DISCLAIMER, f"problem: {problem}"]
    for result in report.results:
        lines.append(format_attack_result(result))
    for hyp in report.hypotheses:
        lines.append(format_hypothesis(hyp))
    for skip in report.skipped:
        lines.append(f"skipped {skip.attack}: {skip.reason}")
    for jump in report.blocked_jumps:
        lines.append(
            f"blocked {jump.id}: {jump.antecedent} => {jump.consequent}"
        )
    return "\n".join(lines) + "\n"


def format_target_report(targets: Sequence[TheoremTarget]) -> str:
    lines = ["exportable theorem targets (not proofs):"]
    exportable = [item for item in targets if item.exportable]
    if not exportable:
        lines.append("  none")
    for item in exportable:
        lines.append(render_yaml(item).rstrip())
    hidden = [item for item in targets if not item.exportable]
    if hidden:
        lines.append("not exported:")
        for item in hidden:
            extra = ""
            if item.kind is ClaimKind.LIVE:
                extra = "; LIVE is not auto-exported"
            lines.append(
                f"  {item.name}: {item.reason} "
                f"({item.scope.value} {item.kind.value}{extra})"
            )
    return "\n".join(lines) + "\n"
