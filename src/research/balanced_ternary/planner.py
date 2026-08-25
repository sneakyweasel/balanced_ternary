"""Deterministic doubled-trit and expanding-D planner sessions."""

from __future__ import annotations

from typing import cast

from research.balanced_ternary.expanding_spec import ExpandingDResidueSpec, expanding_d_spec
from research.balanced_ternary.spec import DoubledTritSpec, doubled_trit_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

CLOSURE_HYPOTHESIS = Hypothesis(
    id="balanced_ternary_finite_closure",
    statement="reachable doubled-trit carries lie in {-1,0,1}",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="balanced_ternary",
)

EXPANDING_CLOSURE_HYPOTHESIS = Hypothesis(
    id="expanding_d_lsd_closure",
    statement="LSD residual of T(n)=3n-lsd(n) is exactly {-1,0,1}",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="expanding_d",
)


def balanced_ternary_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    return ledger


def plan_doubled_trit(
    remaining: int = 8,
    gain: int = 1,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    """Run cheap attacks. Finite-horizon recon is never promoted to R_∞."""
    session = ledger if ledger is not None else balanced_ternary_ledger()
    spec = doubled_trit_spec(start_remaining=remaining, gain=gain)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if (
        closure is not None
        and "balanced_ternary_finite_closure" in session.hypotheses
        and gain == 1
    ):
        try:
            promote_if_legal(session, "balanced_ternary_finite_closure", closure)
        except LedgerError:
            pass
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )


def plan_gain(gain: int, remaining: int = 8) -> PlannerReport:
    ledger = ResearchLedger()
    spec = DoubledTritSpec(gain=gain, start_remaining=remaining)
    return AttackPlanner(ledger).run(cast(ProblemSpec, spec), spec.attack_context())


def expanding_d_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(EXPANDING_CLOSURE_HYPOTHESIS)
    return ledger


def plan_expanding_d(
    remaining: int = 8,
    gain: int = 1,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    """Run cheap attacks on the discovered LSD residual, not on integer n."""
    session = ledger if ledger is not None else expanding_d_ledger()
    spec = expanding_d_spec(start_remaining=remaining, gain=gain)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if (
        closure is not None
        and "expanding_d_lsd_closure" in session.hypotheses
        and gain == 1
    ):
        try:
            promote_if_legal(session, "expanding_d_lsd_closure", closure)
        except LedgerError:
            pass
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )


def plan_expanding_gain(gain: int, remaining: int = 8) -> PlannerReport:
    ledger = ResearchLedger()
    spec = ExpandingDResidueSpec(gain=gain, start_remaining=remaining)
    return AttackPlanner(ledger).run(cast(ProblemSpec, spec), spec.attack_context())
