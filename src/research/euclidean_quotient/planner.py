"""Planner session for hint-free Euclidean remainder dynamics."""

from __future__ import annotations

from typing import cast

from research.euclidean_quotient.spec import DEFAULT_A, DEFAULT_B, INPUT_LENGTH, euclidean_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop, ResearchSession
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import PlannerReport


def plan_euclidean_session(
    a0: int = DEFAULT_A,
    b0: int = DEFAULT_B,
    remaining: int = INPUT_LENGTH,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
    *,
    record: bool = False,
) -> ResearchSession:
    spec = euclidean_spec(a0, b0, start_remaining=remaining)
    loop = ResearchLoop(ledger if ledger is not None else ResearchLedger())
    return loop.run(
        cast(ProblemSpec, spec),
        spec.attack_context(),
        corpus,
        prior_art_status=PriorArtStatus.KNOWN.value,
        record=record,
    )


def plan_euclidean(
    a0: int = DEFAULT_A,
    b0: int = DEFAULT_B,
    remaining: int = INPUT_LENGTH,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
) -> PlannerReport:
    return plan_euclidean_session(a0, b0, remaining, ledger, corpus).attack_report
