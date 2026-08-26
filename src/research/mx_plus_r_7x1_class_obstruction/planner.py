"""Planner session. Unmodified ResearchLoop on the existing mx+r spec."""

from __future__ import annotations

from typing import cast

from research.mx_plus_r_7x1_class_obstruction.spec import map_spec
from research.mx_plus_r.spec import MxPlusRSpec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop, ResearchSession
from research_engine.memory.store import ResearchMemory
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import PlannerReport
from research_engine.strategy import ResearchGoal, StrategyPlanner
from research_engine.strategy.types import StrategyReport


def plan_map_session(
    spec: MxPlusRSpec | None = None,
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
    spec: MxPlusRSpec | None = None,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
) -> PlannerReport:
    return plan_map_session(spec, ledger, corpus).attack_report


def plan_strategy(
    spec: MxPlusRSpec | None = None,
    *,
    goal: ResearchGoal = ResearchGoal.CYCLE_EXCLUSION,
    memory: ResearchMemory | None = None,
) -> StrategyReport:
    """Blind StrategyPlanner entry. Default goal selects census_obstruction."""

    target = spec if spec is not None else map_spec()
    planner = StrategyPlanner()
    return planner.run(
        cast(ProblemSpec, target),
        target.attack_context(),
        goal=goal,
        memory=memory,
    )
