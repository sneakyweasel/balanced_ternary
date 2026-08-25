"""Planner session for signed-digit residual geometry."""

from __future__ import annotations

from typing import cast

from research.signed_digit_residual_geometry.discovery import (
    geometry_report,
    sign_symmetry_halves_mealy,
    singleton_two_witness,
)
from research.signed_digit_residual_geometry.spec import geometry_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

CLOSURE_HYPOTHESIS = Hypothesis(
    id="sdrg_lambda1_u2_interval",
    statement="origin-reachable residual of F_{1,U_2} is the full interval {-1,0,1}",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual_geometry",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

LATTICE_ALL_U_HYPOTHESIS = Hypothesis(
    id="sdrg_lattice_all_U",
    statement="for every finite U, origin-reachable residual equals λℤ ∩ symmetric invariant interval",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual_geometry",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

SIGN_MEALY_HYPOTHESIS = Hypothesis(
    id="sdrg_sign_halves_mealy",
    statement="sign symmetry of U_m forces M(λ,U_m)=|R|/2",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="signed_digit_residual_geometry",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)


def geometry_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(LATTICE_ALL_U_HYPOTHESIS)
    ledger.add_hypothesis(SIGN_MEALY_HYPOTHESIS)
    return ledger


def plan_signed_digit_residual_geometry(
    remaining: int = 8,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else geometry_ledger()
    spec = geometry_spec(start_remaining=remaining)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is not None and "sdrg_lambda1_u2_interval" in session.hypotheses:
        try:
            promote_if_legal(session, "sdrg_lambda1_u2_interval", closure)
        except LedgerError:
            pass

    witness = singleton_two_witness()
    if (
        witness["missing"] == (-1,)
        and "sdrg_lattice_all_U" in session.hypotheses
    ):
        session.decide(
            LATTICE_ALL_U_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "U={2} at λ=1 has box [-1,1] but reachable {0,1}",
        )
    lambda2 = geometry_report(2, 2)
    if (
        "sdrg_sign_halves_mealy" in session.hypotheses
        and lambda2["mealy"] == lambda2["reachable_count"]
        and not sign_symmetry_halves_mealy(1, 2)
    ):
        session.decide(
            SIGN_MEALY_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "U_2 has M=|R| at λ=1 and λ=2; sign does not merge states",
        )
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
