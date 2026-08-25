"""Planner session for multiplicative residual universality."""

from __future__ import annotations

from typing import cast

from research.multiplicative_residual.discovery import (
    doubled_product_report,
    three_trit_report,
    two_trit_report,
)
from research.multiplicative_residual.spec import ProductResidualSpec, product_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

CLOSURE_HYPOTHESIS = Hypothesis(
    id="mr_product_u1_closure",
    statement="two-trit product residual of λ=1 equals F_{1,U_1} = {0}",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="multiplicative_residual",
)

FACTOR_COUNT_HYPOTHESIS = Hypothesis(
    id="mr_factor_count_matters",
    statement="three-trit product has a different origin-reachable residual than two-trit product",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="multiplicative_residual",
)

THREE_STATE_HYPOTHESIS = Hypothesis(
    id="mr_three_residual_states",
    statement="the two-trit product machine has a 3-state origin-reachable residual",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="multiplicative_residual",
)


def multiplicative_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(FACTOR_COUNT_HYPOTHESIS)
    ledger.add_hypothesis(THREE_STATE_HYPOTHESIS)
    return ledger


def plan_multiplicative_residual(
    remaining: int = 8,
    gain: int = 1,
    scale: int = 1,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else multiplicative_ledger()
    spec = product_spec(start_remaining=remaining, gain=gain, scale=scale)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if (
        closure is not None
        and "mr_product_u1_closure" in session.hypotheses
        and gain == 1
        and scale == 1
    ):
        try:
            promote_if_legal(session, "mr_product_u1_closure", closure)
        except LedgerError:
            pass

    two = two_trit_report(1)
    three = three_trit_report(1)
    if "mr_factor_count_matters" in session.hypotheses and three["matches_two_trit_reachable"]:
        session.decide(
            FACTOR_COUNT_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "two-trit and three-trit products both reach {0}",
        )
    if "mr_three_residual_states" in session.hypotheses and two["reachable_count"] == 1:
        session.decide(
            THREE_STATE_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "origin-reachable residual has size 1, matching U_1 not addition",
        )
    _ = doubled_product_report(3)
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )


def plan_product_pair(gain: int, scale: int = 1, remaining: int = 8) -> PlannerReport:
    ledger = ResearchLedger()
    spec = ProductResidualSpec(gain=gain, scale=scale, start_remaining=remaining)
    return AttackPlanner(ledger).run(cast(ProblemSpec, spec), spec.attack_context())
