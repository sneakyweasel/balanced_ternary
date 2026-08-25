"""Planner session for the N∘I₀∘D benchmark."""

from __future__ import annotations

from typing import cast

from research.operator_dynamics.signed_p0.discovery import (
    distinct_orbits_witness,
    envelope_versus_orbit,
    f2_p0_counterexample,
    interval_leak_witness,
    lyapunov_n_witness,
    orbit_of,
)
from research.operator_dynamics.signed_p0.spec import DEFAULT_START, signed_p0_spec
from research_engine.attacks.separation import separate_states
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

PROBLEM_ID = "operator_dynamics_benchmark"

CLOSURE_HYPOTHESIS = Hypothesis(
    id="od_seed_orbit_finite",
    statement="the reachable orbit of the seed under N∘I_0∘D is a finite exact residual",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.NEW_FORMULATION,
)

INTERVAL_HYPOTHESIS = Hypothesis(
    id="od_interval_invariant",
    statement="the integer box |n|≤2 is invariant under N∘I_0∘D",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

LYAPUNOV_HYPOTHESIS = Hypothesis(
    id="od_lyapunov_n",
    statement="V(n)=n strictly decreases on every step",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

GLOBAL_RESIDUAL_HYPOTHESIS = Hypothesis(
    id="od_global_finite_residual",
    statement="the integer n is a single finite residual of N∘I_0∘D on Z",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

F2_HYPOTHESIS = Hypothesis(
    id="od_f2_equals_p0",
    statement="F² = P_0 for F = N∘I_0∘D",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.NEW_FORMULATION,
)

SIGN_MERGE_HYPOTHESIS = Hypothesis(
    id="od_sign_merge",
    statement="distinct positive points on one orbit are sign-equivalent",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)


def signed_p0_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(INTERVAL_HYPOTHESIS)
    ledger.add_hypothesis(LYAPUNOV_HYPOTHESIS)
    ledger.add_hypothesis(GLOBAL_RESIDUAL_HYPOTHESIS)
    ledger.add_hypothesis(F2_HYPOTHESIS)
    ledger.add_hypothesis(SIGN_MERGE_HYPOTHESIS)
    return ledger


def plan_signed_p0(
    remaining: int = 8,
    start: int = DEFAULT_START,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else signed_p0_ledger()
    spec = signed_p0_spec(start_remaining=remaining, start=start)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is not None and CLOSURE_HYPOTHESIS.id in session.hypotheses:
        try:
            promote_if_legal(session, CLOSURE_HYPOTHESIS.id, closure)
        except LedgerError:
            pass

    leak_src, leak_image = interval_leak_witness()
    if INTERVAL_HYPOTHESIS.id in session.hypotheses:
        session.decide(
            INTERVAL_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            f"F({leak_src})={leak_image} leaves |n|≤2",
        )

    lyap = lyapunov_n_witness()
    if LYAPUNOV_HYPOTHESIS.id in session.hypotheses:
        session.decide(
            LYAPUNOV_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            f"V(n)=n does not decrease at n={lyap}: F({lyap})={spec.transition((lyap,), 0, spec.initial_phase())[0]}",
        )

    left, right = distinct_orbits_witness()
    if GLOBAL_RESIDUAL_HYPOTHESIS.id in session.hypotheses:
        session.decide(
            GLOBAL_RESIDUAL_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            f"orbits of {left} and {right} are disjoint; the union over Z is infinite",
        )

    counter = f2_p0_counterexample()
    if F2_HYPOTHESIS.id in session.hypotheses:
        if counter is None:
            session.decide(
                F2_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to F²=P_0 on the probe window; Lean signedP0_sq_eq_P0",
            )
        else:
            session.decide(
                F2_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"F²({counter}) != P_0({counter})",
            )

    orbit = orbit_of(start)
    positives = [n for n in orbit if n > 0]
    if SIGN_MERGE_HYPOTHESIS.id in session.hypotheses and len(positives) >= 2:
        merge = separate_states(spec, (positives[0],), (positives[1],))
        if merge.separated is False and merge.scope is SearchScope.EXACT:
            session.decide(
                SIGN_MERGE_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                f"{positives[0]} and {positives[1]} have identical sign streams",
            )
        elif merge.separated:
            session.decide(
                SIGN_MERGE_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"word {merge.witness_word!r} separates {positives[0]} from {positives[1]}",
            )

    envelope_versus_orbit(start)
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
