"""Planner session for hint-free companion-window maps. Unmodified ResearchLoop."""

from __future__ import annotations

from typing import cast

from research.positivity_lrs.spec import CompanionObsSpec, map_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop, ResearchSession
from research_engine.memory.store import ResearchMemory
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import PlannerReport


def plan_map_session(
    spec: CompanionObsSpec | None = None,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
    *,
    record: bool = False,
    prior_art_status: str = PriorArtStatus.KNOWN.value,
    memory: ResearchMemory | None = None,
) -> ResearchSession:
    target = spec if spec is not None else map_spec()
    loop = ResearchLoop(ledger if ledger is not None else ResearchLedger())
    return loop.run(
        cast(ProblemSpec, target),
        target.attack_context(),
        corpus,
        prior_art_status=prior_art_status,
        record=record,
        memory=memory,
    )


def plan_map(
    spec: CompanionObsSpec | None = None,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
) -> PlannerReport:
    return plan_map_session(spec, ledger, corpus).attack_report
