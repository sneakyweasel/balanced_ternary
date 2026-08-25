"""Planner session for a hint-free accelerated (mx+r) map."""

from __future__ import annotations

from typing import cast

from research.mx_plus_r.spec import DEFAULT_START, INPUT_LENGTH, mx_plus_r_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop, ResearchSession
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import PlannerReport


def plan_mx_plus_r_session(
    m: int,
    r: int,
    remaining: int = INPUT_LENGTH,
    start: int = DEFAULT_START,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
    *,
    record: bool = False,
) -> ResearchSession:
    spec = mx_plus_r_spec(m, r, start_remaining=remaining, start=start)
    loop = ResearchLoop(ledger if ledger is not None else ResearchLedger())
    return loop.run(
        cast(ProblemSpec, spec),
        spec.attack_context(),
        corpus,
        prior_art_status=PriorArtStatus.KNOWN.value,
        record=record,
    )


def plan_mx_plus_r(
    m: int,
    r: int,
    remaining: int = INPUT_LENGTH,
    start: int = DEFAULT_START,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
) -> PlannerReport:
    return plan_mx_plus_r_session(m, r, remaining, start, ledger, corpus).attack_report
