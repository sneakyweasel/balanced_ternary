"""Planner session for a hint-free one-variable loop. Unmodified ResearchLoop."""

from __future__ import annotations

from typing import cast

from research.linear_constraint_loops.spec import OneVariableLoopSpec, RelationLoopSpec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop, ResearchSession
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import PlannerReport


def plan_loop_session(
    spec: OneVariableLoopSpec | RelationLoopSpec,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
    *,
    record: bool = False,
    prior_art_status: str = PriorArtStatus.KNOWN.value,
) -> ResearchSession:
    loop = ResearchLoop(ledger if ledger is not None else ResearchLedger())
    return loop.run(
        cast(ProblemSpec, spec),
        spec.attack_context(),
        corpus,
        prior_art_status=prior_art_status,
        record=record,
    )


def plan_loop(
    spec: OneVariableLoopSpec | RelationLoopSpec,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
) -> PlannerReport:
    return plan_loop_session(spec, ledger, corpus).attack_report
