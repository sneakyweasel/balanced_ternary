"""Planner session for the accelerated odd-only map."""

from __future__ import annotations

from typing import cast

from research.syracuse.discovery import (
    idempotent_counterexample,
    interval_leak_witness,
    lyapunov_n_witness,
    magnitude_drop_counterexample,
    orbit_of,
)
from research.syracuse.spec import DEFAULT_START, syracuse_spec, syracuse_step
from research_engine.attacks.separation import separate_states
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus, PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import PlannerReport

PROBLEM_ID = "syracuse"

CLOSURE_HYPOTHESIS = Hypothesis(
    id="syr_seed_orbit_finite",
    statement="the reachable orbit of the seed is a finite exact residual",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

INTERVAL_HYPOTHESIS = Hypothesis(
    id="syr_interval_invariant",
    statement="the odd integers in [1, 15] are invariant",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

LYAPUNOV_HYPOTHESIS = Hypothesis(
    id="syr_lyapunov_n",
    statement="V(n)=n strictly decreases on every step",
    kind=ClaimKind.LIVE_SLICE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

GLOBAL_RESIDUAL_HYPOTHESIS = Hypothesis(
    id="syr_global_finite_residual",
    statement="the odd positive integers form one finite residual",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

CONTRACTION_HYPOTHESIS = Hypothesis(
    id="syr_contraction_ge3",
    statement="S(n) < n whenever n ≥ 3 is odd",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)

IDEMPOTENT_HYPOTHESIS = Hypothesis(
    id="syr_idempotent",
    statement="S is idempotent: S² = S",
    kind=ClaimKind.REACHABLE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.OPEN,
    problem=PROBLEM_ID,
    prior_art_status=PriorArtStatus.PROJECT_SPECIFIC,
)


def syracuse_ledger() -> ResearchLedger:
    ledger = ResearchLedger()
    ledger.add_hypothesis(CLOSURE_HYPOTHESIS)
    ledger.add_hypothesis(INTERVAL_HYPOTHESIS)
    ledger.add_hypothesis(LYAPUNOV_HYPOTHESIS)
    ledger.add_hypothesis(GLOBAL_RESIDUAL_HYPOTHESIS)
    ledger.add_hypothesis(CONTRACTION_HYPOTHESIS)
    ledger.add_hypothesis(IDEMPOTENT_HYPOTHESIS)
    return ledger


def plan_syracuse_session(
    remaining: int = 12,
    start: int = DEFAULT_START,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
):
    session_ledger = ledger if ledger is not None else syracuse_ledger()
    spec = syracuse_spec(start_remaining=remaining, start=start)
    loop = ResearchLoop(session_ledger)
    return loop.run(
        cast(ProblemSpec, spec),
        spec.attack_context(),
        corpus,
        prior_art_status=PriorArtStatus.KNOWN.value,
        record=False,
    )


def plan_syracuse(
    remaining: int = 12,
    start: int = DEFAULT_START,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
) -> PlannerReport:
    session_ledger = ledger if ledger is not None else syracuse_ledger()
    spec = syracuse_spec(start_remaining=remaining, start=start)
    research = plan_syracuse_session(remaining, start, session_ledger, corpus)
    report = research.attack_report
    closure = next((item for item in report.results if item.name == "closure"), None)
    if closure is not None and CLOSURE_HYPOTHESIS.id in session_ledger.hypotheses:
        if closure.scope is SearchScope.BOUNDED:
            session_ledger.decide(
                CLOSURE_HYPOTHESIS.id,
                DecisionKind.PARK,
                "integer-state BFS hit the cap; this is not a finite-closure theorem",
            )

    leak = interval_leak_witness()
    if INTERVAL_HYPOTHESIS.id in session_ledger.hypotheses:
        if leak is None:
            session_ledger.decide(
                INTERVAL_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no leak of the odd box [1,15] on the probe window",
            )
        else:
            session_ledger.decide(
                INTERVAL_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"S({leak[0]})={leak[1]} leaves the odd box [1,15]",
            )

    lyap = lyapunov_n_witness()
    if LYAPUNOV_HYPOTHESIS.id in session_ledger.hypotheses:
        session_ledger.decide(
            LYAPUNOV_HYPOTHESIS.id,
            DecisionKind.REFUTE,
            f"V(n)=n does not decrease at n={lyap}: S({lyap})={syracuse_step(lyap)}",
        )

    if GLOBAL_RESIDUAL_HYPOTHESIS.id in session_ledger.hypotheses:
        session_ledger.decide(
            GLOBAL_RESIDUAL_HYPOTHESIS.id,
            DecisionKind.PARK,
            "integer-state BFS hit the cap; this is not a finite-residual theorem",
        )

    drop = magnitude_drop_counterexample(min_n=3)
    if CONTRACTION_HYPOTHESIS.id in session_ledger.hypotheses:
        if drop is None:
            session_ledger.decide(
                CONTRACTION_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to S(n)<n for odd n≥3 on the probe window",
            )
        else:
            session_ledger.decide(
                CONTRACTION_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"S({drop})={syracuse_step(drop)} is not < {drop}",
            )

    idem = idempotent_counterexample()
    if IDEMPOTENT_HYPOTHESIS.id in session_ledger.hypotheses:
        if idem is None:
            session_ledger.decide(
                IDEMPOTENT_HYPOTHESIS.id,
                DecisionKind.PROMOTE,
                "no counterexample to S²=S on the probe window",
            )
        else:
            session_ledger.decide(
                IDEMPOTENT_HYPOTHESIS.id,
                DecisionKind.REFUTE,
                f"S(S({idem}))={syracuse_step(syracuse_step(idem))} != S({idem})",
            )

    orbit_of(start)
    separate_states(spec, spec.initial_state, (syracuse_step(start),))
    return PlannerReport(
        results=report.results,
        skipped=report.skipped,
        hypotheses=tuple(session_ledger.hypotheses.values()),
        blocked_jumps=report.blocked_jumps,
        next_attacks=report.next_attacks,
    )
