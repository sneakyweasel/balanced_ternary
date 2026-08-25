"""Planner session for signed-digit residual phase transitions."""

from __future__ import annotations

from typing import cast

from research.signed_digit_residual.discovery import (
    finite_from_origin,
    geometry_perturbation,
    is_constant_unbounded_family,
    origin_reachable_report,
)
from research.signed_digit_residual.spec import SignedDigitResidualSpec, signed_digit_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

CLOSURE_HYPOTHESIS = Hypothesis(
    id="sdr_lambda1_u2_closure",
    statement="origin-reachable residual of F_{1,U_2} is exactly {-1,0,1}",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

SCALAR_THRESHOLD_HYPOTHESIS = Hypothesis(
    id="sdr_scalar_lambda3",
    statement="gain λ=3 forces unbounded residual independently of U",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

GEOMETRY_PHASE_HYPOTHESIS = Hypothesis(
    id="sdr_geometry_controls_phase",
    statement="holes or asymmetry in U change the finite/infinite residual phase at fixed (λ, max|u|)",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

MAXABS_MEALY_HYPOTHESIS = Hypothesis(
    id="sdr_maxabs_determines_mealy",
    statement="minimal residual complexity M(λ,U) is determined by (λ, max|u|) alone",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)


def signed_digit_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(SCALAR_THRESHOLD_HYPOTHESIS)
    ledger.add_hypothesis(GEOMETRY_PHASE_HYPOTHESIS)
    ledger.add_hypothesis(MAXABS_MEALY_HYPOTHESIS)
    return ledger


def plan_signed_digit_residual(
    remaining: int = 8,
    bound: int = 2,
    gain: int = 1,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else signed_digit_ledger()
    spec = signed_digit_spec(start_remaining=remaining, bound=bound, gain=gain)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if (
        closure is not None
        and "sdr_lambda1_u2_closure" in session.hypotheses
        and gain == 1
        and bound == 2
    ):
        try:
            promote_if_legal(session, "sdr_lambda1_u2_closure", closure)
        except LedgerError:
            pass

    three_one = origin_reachable_report(1, 3)
    if (
        three_one["classification"] == "EXACT FINITE"
        and three_one["reachable"] == (0,)
        and "sdr_scalar_lambda3" in session.hypotheses
    ):
        session.decide(
            SCALAR_THRESHOLD_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "F_{3,U_1} stays at 0; λ=3 is not independently infinite",
        )
    geometry = geometry_perturbation()
    if (
        geometry["sparse_2_g1"]["classification"] == "EXACT FINITE"
        and geometry["sparse_2_g3"]["classification"] == "EXACT INFINITE"
        and geometry["asymmetric_012_g1"]["classification"] == "EXACT FINITE"
        and geometry["asymmetric_012_g3"]["classification"] == "EXACT INFINITE"
        and "sdr_geometry_controls_phase" in session.hypotheses
    ):
        session.decide(
            GEOMETRY_PHASE_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "phase follows (λ, max|u|); {-2,0,2} and {0,1,2} match U_2",
        )
    if (
        geometry["singleton_2_g2"]["mealy"] == 2
        and origin_reachable_report(2, 2)["mealy"] == 3
        and "sdr_maxabs_determines_mealy" in session.hypotheses
    ):
        session.decide(
            MAXABS_MEALY_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "U={2} at λ=2 has Mealy 2 while U_2 has Mealy 3",
        )
    _ = finite_from_origin(1, 2)
    _ = is_constant_unbounded_family(2, 3)
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )


def plan_signed_digit_pair(gain: int, bound: int, remaining: int = 8) -> PlannerReport:
    ledger = ResearchLedger()
    spec = SignedDigitResidualSpec(gain=gain, bound=bound, start_remaining=remaining)
    return AttackPlanner(ledger).run(cast(ProblemSpec, spec), spec.attack_context())
