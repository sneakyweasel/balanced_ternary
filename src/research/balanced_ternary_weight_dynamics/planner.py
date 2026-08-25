"""Planner session for the weight-dynamics control experiment."""

from __future__ import annotations

from typing import cast

from research.balanced_ternary_weight_dynamics.discovery import (
    distinct_orbits_witness,
    envelope_versus_orbit,
    even_map_counterexample,
    idempotent_counterexample,
    interval_leak_witness,
    lyapunov_n_witness,
    magnitude_drop_counterexample,
    orbit_of,
)
from research.balanced_ternary_weight_dynamics.spec import (
    DEFAULT_START,
    digit_square_sum,
    weight_dynamics_spec,
)
from research_engine.attacks.separation import separate_states
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

PROBLEM_ID = "balanced_ternary_weight_dynamics"

CLOSURE_HYPOTHESIS = Hypothesis(
    id="wd_seed_orbit_finite",
    statement="the reachable orbit of the seed under T(n)=W(n) is a finite exact residual",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.KNOWN,
)

INTERVAL_HYPOTHESIS = Hypothesis(
    id="wd_interval_invariant",
    statement="the integer box |n|≤2 is invariant under T(n)=W(n)",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

LYAPUNOV_HYPOTHESIS = Hypothesis(
    id="wd_lyapunov_n",
    statement="V(n)=n strictly decreases on every step",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

GLOBAL_RESIDUAL_HYPOTHESIS = Hypothesis(
    id="wd_global_finite_residual",
    statement="the integer n is a single finite residual of T(n)=W(n) on Z",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

IDENTITY_MERGE_HYPOTHESIS = Hypothesis(
    id="wd_identity_merge",
    statement="identity observation merges distinct points of one seed orbit",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

IDEMPOTENT_HYPOTHESIS = Hypothesis(
    id="wd_idempotent",
    statement="T is idempotent: T² = T",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

CONTRACTION_GE2_HYPOTHESIS = Hypothesis(
    id="wd_contraction_ge2",
    statement="|T(n)| < |n| whenever |n| ≥ 2",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

CONTRACTION_GE3_HYPOTHESIS = Hypothesis(
    id="wd_contraction_ge3",
    statement="|T(n)| < |n| whenever |n| ≥ 3",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.KNOWN,
)

EVEN_HYPOTHESIS = Hypothesis(
    id="wd_even",
    statement="T(-n) = T(n)",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.KNOWN,
)


def weight_dynamics_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(INTERVAL_HYPOTHESIS)
    ledger.add_hypothesis(LYAPUNOV_HYPOTHESIS)
    ledger.add_hypothesis(GLOBAL_RESIDUAL_HYPOTHESIS)
    ledger.add_hypothesis(IDENTITY_MERGE_HYPOTHESIS)
    ledger.add_hypothesis(IDEMPOTENT_HYPOTHESIS)
    ledger.add_hypothesis(CONTRACTION_GE2_HYPOTHESIS)
    ledger.add_hypothesis(CONTRACTION_GE3_HYPOTHESIS)
    ledger.add_hypothesis(EVEN_HYPOTHESIS)
    return ledger


def plan_weight_dynamics(
    remaining: int = 8,
    start: int = DEFAULT_START,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else weight_dynamics_ledger()
    spec = weight_dynamics_spec(start_remaining=remaining, start=start)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is not None and CLOSURE_HYPOTHESIS.id in session.hypotheses:
        try:
            promote_if_legal(session, CLOSURE_HYPOTHESIS.id, closure)
        except LedgerError:
            pass

    leak = interval_leak_witness()
    if INTERVAL_HYPOTHESIS.id in session.hypotheses:
        if leak is None:
            session.decide(
                INTERVAL_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "exhaustive check of the finite box |n|≤2 finds no one-step leak",
            )
        else:
            session.decide(
                INTERVAL_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"T({leak[0]})={leak[1]} leaves |n|≤2",
            )

    lyap = lyapunov_n_witness()
    if LYAPUNOV_HYPOTHESIS.id in session.hypotheses:
        session.decide(
            LYAPUNOV_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            f"V(n)=n does not decrease at n={lyap}: T({lyap})={digit_square_sum(lyap)}",
        )

    left, right = distinct_orbits_witness()
    if GLOBAL_RESIDUAL_HYPOTHESIS.id in session.hypotheses:
        session.decide(
            GLOBAL_RESIDUAL_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            f"orbits of {left} and {right} are disjoint; the union over Z is infinite",
        )

    orbit = orbit_of(start)
    if IDENTITY_MERGE_HYPOTHESIS.id in session.hypotheses and len(orbit) >= 2:
        merge = separate_states(spec, (orbit[0],), (orbit[1],))
        if merge.separated is False and merge.scope is SearchScope.EXACT:
            session.decide(
                IDENTITY_MERGE_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                f"{orbit[0]} and {orbit[1]} have identical identity streams",
            )
        elif merge.separated:
            session.decide(
                IDENTITY_MERGE_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"word {merge.witness_word!r} separates {orbit[0]} from {orbit[1]}",
            )

    idem = idempotent_counterexample()
    if IDEMPOTENT_HYPOTHESIS.id in session.hypotheses:
        if idem is None:
            session.decide(
                IDEMPOTENT_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to T²=T on the probe window",
            )
        else:
            session.decide(
                IDEMPOTENT_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"T(T({idem}))={digit_square_sum(digit_square_sum(idem))} != T({idem})={digit_square_sum(idem)}",
            )

    drop2 = magnitude_drop_counterexample(min_abs=2)
    if CONTRACTION_GE2_HYPOTHESIS.id in session.hypotheses:
        if drop2 is None:
            session.decide(
                CONTRACTION_GE2_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to |T(n)|<|n| for |n|≥2 on the probe window",
            )
        else:
            session.decide(
                CONTRACTION_GE2_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"|T({drop2})|={abs(digit_square_sum(drop2))} is not < |{drop2}|",
            )

    drop3 = magnitude_drop_counterexample(min_abs=3)
    if CONTRACTION_GE3_HYPOTHESIS.id in session.hypotheses:
        if drop3 is None:
            session.decide(
                CONTRACTION_GE3_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to |T(n)|<|n| for |n|≥3 on the probe window; Lean weightZ_natAbs_lt",
            )
        else:
            session.decide(
                CONTRACTION_GE3_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"|T({drop3})|={abs(digit_square_sum(drop3))} is not < |{drop3}|",
            )

    even = even_map_counterexample()
    if EVEN_HYPOTHESIS.id in session.hypotheses:
        if even is None:
            session.decide(
                EVEN_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to T(-n)=T(n) on the probe window; Lean weightZ_even",
            )
        else:
            session.decide(
                EVEN_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"T(-{even})={digit_square_sum(-even)} != T({even})={digit_square_sum(even)}",
            )

    envelope_versus_orbit(start)
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
