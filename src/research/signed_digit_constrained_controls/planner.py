"""Planner session for signed-digit constrained controls."""

from __future__ import annotations

from typing import cast

from research.signed_digit_constrained_controls.discovery import (
    constant_word_is_required,
    residual_merge_exists,
)
from research.signed_digit_constrained_controls.spec import constrained_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

CLOSURE_HYPOTHESIS = Hypothesis(
    id="sdrc_norepeat_u2_product",
    statement="no-repeat control on F_{1,U_2} has a 10-state origin-reachable product",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_constrained_controls",
)

CONSTANT_HYPOTHESIS = Hypothesis(
    id="sdrc_need_constant",
    statement="3-adic residual rigidity requires a common cyclic/constant legal letter",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_constrained_controls",
)

MERGE_HYPOTHESIS = Hypothesis(
    id="sdrc_residual_merge",
    statement="some Model A–D constraint merges distinct residuals at the same control state",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_constrained_controls",
)


def constrained_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(CONSTANT_HYPOTHESIS)
    ledger.add_hypothesis(MERGE_HYPOTHESIS)
    return ledger


def plan_signed_digit_constrained_controls(
    remaining: int = 8,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else constrained_ledger()
    spec = constrained_spec(start_remaining=remaining)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is not None and "sdrc_norepeat_u2_product" in session.hypotheses:
        try:
            promote_if_legal(session, "sdrc_norepeat_u2_product", closure)
        except LedgerError:
            pass

    if not constant_word_is_required() and "sdrc_need_constant" in session.hypotheses:
        session.decide(
            CONSTANT_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "no-repeat forbids constant words but the product remains Mealy-minimal",
        )
    if not residual_merge_exists() and "sdrc_residual_merge" in session.hypotheses:
        session.decide(
            MERGE_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "Models A–D never merge distinct residuals at one control state",
        )
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
