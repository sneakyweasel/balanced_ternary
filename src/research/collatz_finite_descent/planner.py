"""Planner session for shortcut Collatz finite-descent reconnaissance."""

from __future__ import annotations

from typing import cast

from research.collatz_finite_descent.blocks import expanding_legal_witness, one_step_lyapunov_witness
from research.collatz_finite_descent.spec import shortcut_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport

UNIFORM_DESCENT_HYPOTHESIS = Hypothesis(
    id="collatz_uniform_L_descent",
    statement=(
        "Every n > N0 has a contracting shortcut block of length at most L "
        "determined by n mod 2^L"
    ),
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="collatz_finite_descent",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

ONE_STEP_LYAPUNOV_HYPOTHESIS = Hypothesis(
    id="collatz_one_step_lyapunov",
    statement="V(n)=n strictly decreases on every shortcut step",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="collatz_finite_descent",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

INTEGER_RESIDUAL_HYPOTHESIS = Hypothesis(
    id="collatz_integer_finite_residual",
    statement="The integer n is a finite residual of shortcut Collatz",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="collatz_finite_descent",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)


def collatz_finite_descent_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(UNIFORM_DESCENT_HYPOTHESIS)
    ledger.add_hypothesis(ONE_STEP_LYAPUNOV_HYPOTHESIS)
    ledger.add_hypothesis(INTEGER_RESIDUAL_HYPOTHESIS)
    return ledger


def plan_collatz_finite_descent(
    remaining: int = 12,
    odd_mul: int = 3,
    odd_add: int = 1,
    start: int = 27,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else collatz_finite_descent_ledger()
    spec = shortcut_spec(
        start_remaining=remaining,
        odd_mul=odd_mul,
        odd_add=odd_add,
        start=start,
    )
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    length = max(1, remaining)
    witness, image, word = expanding_legal_witness(length, odd_mul, odd_add)
    session.decide(
        UNIFORM_DESCENT_HYPOTHESIS.id,
        DecisionKind.REFUTE,
        f"n={witness} word={''.join(word)}; C^{length}(n)={image} >= n",
    )
    lyapunov_n = one_step_lyapunov_witness(odd_mul, odd_add)
    session.decide(
        ONE_STEP_LYAPUNOV_HYPOTHESIS.id,
        DecisionKind.REFUTE,
        f"odd n={lyapunov_n} does not decrease",
    )
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is not None and closure.scope is SearchScope.BOUNDED:
        session.decide(
            INTEGER_RESIDUAL_HYPOTHESIS.id,
            DecisionKind.PARK,
            "integer-state BFS hit the cap; this is not a finite-closure theorem",
        )
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )


def plan_perturbation_5_1(remaining: int = 12) -> PlannerReport:
    return plan_collatz_finite_descent(remaining=remaining, odd_mul=5, odd_add=1)


def plan_terminal_cycle(remaining: int = 8) -> PlannerReport:
    from research.collatz_finite_descent.spec import terminal_spec

    spec = terminal_spec(remaining)
    return AttackPlanner().run(cast(ProblemSpec, spec), spec.attack_context())
