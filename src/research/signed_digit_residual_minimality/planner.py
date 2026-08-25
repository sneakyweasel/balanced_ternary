"""Planner session for signed-digit residual minimality."""

from __future__ import annotations

from typing import cast

from research.signed_digit_residual_minimality.discovery import (
    first_merge,
    mod3_does_not_merge,
    search_is_minimal,
)
from research.signed_digit_residual_minimality.spec import minimality_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

CLOSURE_HYPOTHESIS = Hypothesis(
    id="sdrm_lambda1_u2_minimal",
    statement="origin-reachable residual of F_{1,U_2} is a 3-state minimal Mealy machine",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual_minimality",
)

MERGE_HYPOTHESIS = Hypothesis(
    id="sdrm_merge_exists",
    statement="some listed finite U at λ=1 or λ=2 has M(λ,U)<|R_{λ,U}|",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual_minimality",
)

MOD3_HYPOTHESIS = Hypothesis(
    id="sdrm_mod3_merges",
    statement="identical immediate lsd signatures force behavioral equivalence",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual_minimality",
)


def minimality_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(MERGE_HYPOTHESIS)
    ledger.add_hypothesis(MOD3_HYPOTHESIS)
    return ledger


def plan_signed_digit_residual_minimality(
    remaining: int = 8,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else minimality_ledger()
    spec = minimality_spec(start_remaining=remaining)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is not None and "sdrm_lambda1_u2_minimal" in session.hypotheses:
        try:
            promote_if_legal(session, "sdrm_lambda1_u2_minimal", closure)
        except LedgerError:
            pass

    if search_is_minimal() and "sdrm_merge_exists" in session.hypotheses:
        session.decide(
            MERGE_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "every listed U at λ=1 and λ=2 has singleton Mealy classes",
        )
    if (
        first_merge() is None
        and mod3_does_not_merge()
        and "sdrm_mod3_merges" in session.hypotheses
    ):
        session.decide(
            MOD3_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "0 and 3 at λ=1 share the 1-letter signature but are separated by (0,0)",
        )
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
