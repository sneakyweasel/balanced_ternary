"""Planner session for prime residual complexity."""

from __future__ import annotations

from typing import cast

from research.prime_residual_complexity.distinguish import (
    MAX_HORIZON,
    MAX_LENGTH,
    jet_prime_separator,
    residual_table,
    sieve_prime_separator,
)
from research.prime_residual_complexity.sieve import sieve_chain_census
from research.prime_residual_complexity.spec import prime_spec, sieve_spec
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import (
    AttackPlanner,
    PlannerReport,
    promote_if_legal,
    run_named_attack,
)

SIEVE_RESIDUAL_HYPOTHESIS = Hypothesis(
    id="prc_sieve_finite_residual",
    statement="The LSD-first BT DFA for gcd(n, M)=1 with M=2·3·5·7 is a finite residual",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="prime_residual_complexity",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

JET_EQUALS_PRIME_HYPOTHESIS = Hypothesis(
    id="prc_jet_equals_prime",
    statement="Equal length-L LSD jets have identical Prime continuation behaviour",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="prime_residual_complexity",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

SIEVE_EQUALS_PRIME_HYPOTHESIS = Hypothesis(
    id="prc_sieve_equals_prime",
    statement="The finite sieve residual gcd(n, M)=1 equals the Prime residual",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="prime_residual_complexity",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

INTEGER_PRIME_HYPOTHESIS = Hypothesis(
    id="prc_integer_prime_residual",
    statement="The integer n is a finite residual of the Prime section dynamics",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem="prime_residual_complexity",
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)


def prime_residual_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(SIEVE_RESIDUAL_HYPOTHESIS)
    ledger.add_hypothesis(JET_EQUALS_PRIME_HYPOTHESIS)
    ledger.add_hypothesis(SIEVE_EQUALS_PRIME_HYPOTHESIS)
    ledger.add_hypothesis(INTEGER_PRIME_HYPOTHESIS)
    return ledger


def plan_prime_residual_complexity(
    remaining: int = 4,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else prime_residual_ledger()
    depth = max(1, remaining)
    spec = sieve_spec(start_remaining=depth)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if (
        closure is not None
        and closure.status is AttackStatus.SUPPORTED
        and closure.scope is SearchScope.EXACT
    ):
        promote_if_legal(session, SIEVE_RESIDUAL_HYPOTHESIS.id, closure)

    jet_witness = jet_prime_separator(length=min(depth, MAX_LENGTH))
    session.decide(
        JET_EQUALS_PRIME_HYPOTHESIS.id,
        DecisionKind.REFUTE,
        (
            f"x={jet_witness.left} y={jet_witness.right} word={jet_witness.word}; "
            f"Prime({jet_witness.left_image})={jet_witness.left_prime} "
            f"Prime({jet_witness.right_image})={jet_witness.right_prime}"
        ),
    )
    sieve_witness = sieve_prime_separator()
    session.decide(
        SIEVE_EQUALS_PRIME_HYPOTHESIS.id,
        DecisionKind.REFUTE,
        (
            f"x={sieve_witness.left} y={sieve_witness.right} word={sieve_witness.word}; "
            f"Prime({sieve_witness.left_image})={sieve_witness.left_prime} "
            f"Prime({sieve_witness.right_image})={sieve_witness.right_prime}"
        ),
    )

    integer_spec = prime_spec(start_remaining=depth)
    integer_closure = run_named_attack(
        "closure",
        cast(ProblemSpec, integer_spec),
        integer_spec.attack_context(),
    )
    if (
        integer_closure.status is AttackStatus.INCONCLUSIVE
        and integer_closure.scope is SearchScope.BOUNDED
    ):
        session.decide(
            INTEGER_PRIME_HYPOTHESIS.id,
            DecisionKind.PARK,
            "integer-state BFS hit the cap; this is not a finite-closure theorem",
        )

    _ = residual_table(min(depth, MAX_LENGTH), min(MAX_HORIZON, 3))
    _ = sieve_chain_census()

    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
