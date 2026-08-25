"""Planner session for the weight-drift experiment."""

from __future__ import annotations

from typing import cast

from research.balanced_ternary_weight_drift.discovery import (
    even_map_counterexample,
    idempotent_counterexample,
    interval_leak_witness,
    lyapunov_n_witness,
    magnitude_drop_counterexample,
    nonpos_invariant_counterexample,
    orbit_intersection_witness,
    orbit_of,
    strict_increase_counterexample,
)
from research.balanced_ternary_weight_drift.spec import (
    DEFAULT_START,
    weight_drift,
    weight_drift_spec,
)
from research_engine.attacks.result import AttackStatus
from research_engine.attacks.separation import separate_states
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport, promote_if_legal

PROBLEM_ID = "balanced_ternary_weight_drift"

CLOSURE_HYPOTHESIS = Hypothesis(
    id="wdr_seed_orbit_finite",
    statement="the reachable orbit of the seed under T(n)=n+W(n) is a finite exact residual",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

INTERVAL_HYPOTHESIS = Hypothesis(
    id="wdr_interval_invariant",
    statement="the integer box |n|≤2 is invariant under T(n)=n+W(n)",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

LYAPUNOV_HYPOTHESIS = Hypothesis(
    id="wdr_lyapunov_n",
    statement="V(n)=n strictly decreases on every step",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

GLOBAL_RESIDUAL_HYPOTHESIS = Hypothesis(
    id="wdr_global_finite_residual",
    statement="the integer n is a single finite residual of T(n)=n+W(n) on Z",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

IDENTITY_MERGE_HYPOTHESIS = Hypothesis(
    id="wdr_identity_merge",
    statement="identity observation merges distinct points of one seed orbit",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

IDEMPOTENT_HYPOTHESIS = Hypothesis(
    id="wdr_idempotent",
    statement="T is idempotent: T² = T",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

CONTRACTION_HYPOTHESIS = Hypothesis(
    id="wdr_contraction",
    statement="|T(n)| < |n| whenever |n| ≥ 2",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

EVEN_HYPOTHESIS = Hypothesis(
    id="wdr_even",
    statement="T(-n) = T(n)",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

DISJOINT_HYPOTHESIS = Hypothesis(
    id="wdr_disjoint_orbits",
    statement="distinct seeds have disjoint forward orbits",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

INCREASE_HYPOTHESIS = Hypothesis(
    id="wdr_strict_increase",
    statement="T(n) > n whenever n ≠ 0",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.KNOWN,
)

NONPOS_HYPOTHESIS = Hypothesis(
    id="wdr_nonpos_invariant",
    statement="T maps nonpositive integers to nonpositive integers",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.KNOWN,
)


def weight_drift_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(INTERVAL_HYPOTHESIS)
    ledger.add_hypothesis(LYAPUNOV_HYPOTHESIS)
    ledger.add_hypothesis(GLOBAL_RESIDUAL_HYPOTHESIS)
    ledger.add_hypothesis(IDENTITY_MERGE_HYPOTHESIS)
    ledger.add_hypothesis(IDEMPOTENT_HYPOTHESIS)
    ledger.add_hypothesis(CONTRACTION_HYPOTHESIS)
    ledger.add_hypothesis(EVEN_HYPOTHESIS)
    ledger.add_hypothesis(DISJOINT_HYPOTHESIS)
    ledger.add_hypothesis(INCREASE_HYPOTHESIS)
    ledger.add_hypothesis(NONPOS_HYPOTHESIS)
    return ledger


def plan_weight_drift(
    remaining: int = 8,
    start: int = DEFAULT_START,
    ledger: ResearchLedger | None = None,
) -> PlannerReport:
    session = ledger if ledger is not None else weight_drift_ledger()
    spec = weight_drift_spec(start_remaining=remaining, start=start)
    report = AttackPlanner(session).run(cast(ProblemSpec, spec), spec.attack_context())
    closure = next((item for item in report.results if item.name == "closure"), None)
    if (
        closure is not None
        and CLOSURE_HYPOTHESIS.id in session.hypotheses
        and closure.status is AttackStatus.SUPPORTED
    ):
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
            f"V(n)=n does not decrease at n={lyap}: T({lyap})={weight_drift(lyap)}",
        )

    if GLOBAL_RESIDUAL_HYPOTHESIS.id in session.hypotheses:
        session.decide(
            GLOBAL_RESIDUAL_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            "positive seed 4 is strictly increasing on the probe; the union over Z is infinite",
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
                f"T(T({idem}))={weight_drift(weight_drift(idem))} != T({idem})={weight_drift(idem)}",
            )

    drop = magnitude_drop_counterexample(min_abs=2)
    if CONTRACTION_HYPOTHESIS.id in session.hypotheses:
        if drop is None:
            session.decide(
                CONTRACTION_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to |T(n)|<|n| for |n|≥2 on the probe window",
            )
        else:
            session.decide(
                CONTRACTION_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"|T({drop})|={abs(weight_drift(drop))} is not < |{drop}|",
            )

    even = even_map_counterexample()
    if EVEN_HYPOTHESIS.id in session.hypotheses:
        if even is None:
            session.decide(
                EVEN_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to T(-n)=T(n) on the probe window",
            )
        else:
            session.decide(
                EVEN_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"T(-{even})={weight_drift(-even)} != T({even})={weight_drift(even)}",
            )

    left, right, meet = orbit_intersection_witness()
    if DISJOINT_HYPOTHESIS.id in session.hypotheses:
        session.decide(
            DISJOINT_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            f"orbits of {left} and {right} meet at {meet}",
        )

    increase = strict_increase_counterexample()
    if INCREASE_HYPOTHESIS.id in session.hypotheses:
        if increase is None:
            session.decide(
                INCREASE_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to T(n)>n for n≠0 on the probe window; Lean weightDriftZ_gt",
            )
        else:
            session.decide(
                INCREASE_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"T({increase})={weight_drift(increase)} is not > {increase}",
            )

    if (
        CLOSURE_HYPOTHESIS.id in session.hypotheses
        and session.hypotheses[CLOSURE_HYPOTHESIS.id].status is HypothesisStatus.OPEN
        and increase is None
        and start > 0
    ):
        session.decide(
            CLOSURE_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            f"seed {start}>0 and T(n)>n for n≠0; the forward orbit is infinite",
        )

    nonpos = nonpos_invariant_counterexample()
    if NONPOS_HYPOTHESIS.id in session.hypotheses:
        if nonpos is None:
            session.decide(
                NONPOS_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to T(n)≤0 for n≤0 on the probe window; Lean weightDriftZ_nonpos",
            )
        else:
            session.decide(
                NONPOS_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"T({nonpos})={weight_drift(nonpos)} is positive",
            )

    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
