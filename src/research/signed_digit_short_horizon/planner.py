"""Planner session for signed-digit short-horizon controls."""

from __future__ import annotations

from typing import cast

from research.signed_digit_short_horizon.discovery import (
    genuine_merge_exists,
    only_deadlock_merges,
    shorter_always_separates,
)
from research.signed_digit_short_horizon.spec import short_horizon_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

CLOSURE_HYPOTHESIS = Hypothesis(
    id="sdsh_horizon_u2_product",
    statement="horizon-2 control on F_{1,U_2} has a 7-state origin-reachable product",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_short_horizon",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

MERGE_HYPOTHESIS = Hypothesis(
    id="sdsh_genuine_merge",
    statement="(0,q_1) and (3,q_1) are observationally equivalent under horizon 1",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_short_horizon",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

SHORT_SEP_HYPOTHESIS = Hypothesis(
    id="sdsh_short_separator",
    statement="some legal word shorter than v_3(s-t)+1 always separates distinct residuals",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_short_horizon",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

DEADLOCK_HYPOTHESIS = Hypothesis(
    id="sdsh_only_deadlock",
    statement="finite horizon creates residual merges only through deadlock",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_short_horizon",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)


def short_horizon_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(MERGE_HYPOTHESIS)
    ledger.add_hypothesis(SHORT_SEP_HYPOTHESIS)
    ledger.add_hypothesis(DEADLOCK_HYPOTHESIS)
    return ledger


def plan_signed_digit_short_horizon(
    remaining: int = 8,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else short_horizon_ledger()
    spec = short_horizon_spec(start_remaining=remaining)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is not None and "sdsh_horizon_u2_product" in session.hypotheses:
        try:
            promote_if_legal(session, "sdsh_horizon_u2_product", closure)
        except LedgerError:
            pass

    if genuine_merge_exists() and "sdsh_genuine_merge" in session.hypotheses:
        session.decide(
            MERGE_HYPOTHESIS.id,
            DecisionKind.PROMOTE,
            "(0,q_1)~(3,q_1): every length-1 word agrees, then both terminate",
        )
    if not shorter_always_separates() and "sdsh_short_separator" in session.hypotheses:
        session.decide(
            SHORT_SEP_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "horizon 1 makes 0 and 3 agree on every legal word",
        )
    if not only_deadlock_merges() and "sdsh_only_deadlock" in session.hypotheses:
        session.decide(
            DEADLOCK_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "the (0,3) merge at horizon 1 takes a legal step before terminating",
        )
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
