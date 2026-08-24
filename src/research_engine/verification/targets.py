"""Minimal Lean theorem targets. Not proofs, and never compiled."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import Any

from research_engine.attacks.result import AttackResult, AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport

FORBIDDEN_LEAN_TOKENS: tuple[str, ...] = ("sorry", "admit")
_SMALL_EVIDENCE: tuple[str, ...] = (
    "horizon",
    "complete",
    "forcing_gcds",
    "block_kind",
    "translation",
    "union_size",
    "fixes_origin",
    "moduli_requested",
)


@dataclass(frozen=True)
class TheoremTarget:
    """A statement a human may formalize. The engine does not prove it."""

    name: str
    statement: str
    kind: ClaimKind
    scope: SearchScope
    exportable: bool
    reason: str
    attack: str = ""
    problem: str = ""
    lean_module: str = ""
    lean_theorem: str = ""
    hypotheses: tuple[str, ...] = ()
    finite_checks: tuple[str, ...] = ()
    certificates: tuple[Any, ...] = ()

    @property
    def linked(self) -> bool:
        return bool(self.lean_module and self.lean_theorem)


def _slug(problem: str, attack: str) -> str:
    prefix = problem.strip() or "anonymous"
    return f"{prefix}_{attack}"


def _finite_checks(result: AttackResult) -> tuple[str, ...]:
    return tuple(
        f"{key}={result.evidence[key]}"
        for key in _SMALL_EVIDENCE
        if key in result.evidence
    )


def target_from_result(result: AttackResult, *, problem: str = "") -> TheoremTarget:
    """Turn one attack outcome into a target.

    Only ``SUPPORTED`` + ``EXACT`` non-``LIVE`` results are exportable.
    Bounded censuses and live-infinitude claims are not.
    """
    name = _slug(problem, result.name)
    checks = _finite_checks(result)
    if result.kind is ClaimKind.LIVE:
        return TheoremTarget(
            name=name,
            statement=result.claim,
            kind=result.kind,
            scope=result.scope,
            exportable=False,
            reason="LIVE claims are not auto-exported",
            attack=result.name,
            problem=problem,
            finite_checks=checks,
            certificates=result.certificates,
        )
    if result.status is AttackStatus.SUPPORTED and result.scope is SearchScope.EXACT:
        return TheoremTarget(
            name=name,
            statement=result.claim,
            kind=result.kind,
            scope=result.scope,
            exportable=True,
            reason="exact supported certificate",
            attack=result.name,
            problem=problem,
            finite_checks=checks,
            certificates=result.certificates,
        )
    return TheoremTarget(
        name=name,
        statement=result.claim,
        kind=result.kind,
        scope=result.scope,
        exportable=False,
        reason="not an exact supported certificate",
        attack=result.name,
        problem=problem,
        finite_checks=checks,
        certificates=result.certificates,
    )


def attach_lean(
    target: TheoremTarget,
    *,
    module: str,
    theorem: str,
    name: str | None = None,
) -> TheoremTarget:
    """Record an already-proved Lean name. Does not generate a proof."""
    return replace(
        target,
        name=name if name is not None else target.name,
        lean_module=module,
        lean_theorem=theorem,
        reason=f"linked to existing {module}.{theorem}",
    )


def targets_from_results(
    results: Sequence[AttackResult],
    *,
    problem: str = "",
) -> tuple[TheoremTarget, ...]:
    return tuple(target_from_result(result, problem=problem) for result in results)


def targets_from_report(report: PlannerReport, *, problem: str = "") -> tuple[TheoremTarget, ...]:
    return targets_from_results(report.results, problem=problem)


def exportable_targets(targets: Sequence[TheoremTarget]) -> tuple[TheoremTarget, ...]:
    return tuple(item for item in targets if item.exportable)


def render_yaml(target: TheoremTarget) -> str:
    linked = f"{target.lean_module}.{target.lean_theorem}" if target.linked else ""
    checks = "; ".join(target.finite_checks)
    return (
        "theorem_target:\n"
        f"  name: {target.name}\n"
        f"  statement: {target.statement}\n"
        f"  kind: {target.kind.value}\n"
        f"  scope: {target.scope.value}\n"
        f"  exportable: {str(target.exportable).lower()}\n"
        f"  reason: {target.reason}\n"
        f"  lean_theorem: {linked}\n"
        f"  finite_checks: {checks}\n"
    )


def render_lean_comment(target: TheoremTarget) -> str:
    """Comment-only skeleton. Never a compilable proof obligation."""
    linked = (
        f"existing: {target.lean_module}.{target.lean_theorem}"
        if target.linked
        else "existing: none"
    )
    body = (
        "/-\n"
        "Lean target (comment only; not compiled; not a proof obligation)\n"
        f"name: {target.name}\n"
        f"statement: {target.statement}\n"
        f"kind: {target.kind.value}\n"
        f"scope: {target.scope.value}\n"
        f"exportable: {target.exportable}\n"
        f"{linked}\n"
        "-/\n"
    )
    assert_no_proof_tokens(body)
    return body


def assert_no_proof_tokens(text: str) -> None:
    lowered = text.lower()
    for token in FORBIDDEN_LEAN_TOKENS:
        if token in lowered:
            raise AssertionError(f"forbidden token {token!r} in generated text")
