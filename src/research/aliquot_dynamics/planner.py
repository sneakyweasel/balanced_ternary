"""Planner session for the hint-free sigma-minus-n map. Unmodified ResearchLoop."""

from __future__ import annotations

from typing import cast

from research.aliquot_dynamics.spec import SigmaMinusNSpec, map_spec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop, ResearchSession
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import PlannerReport


def plan_map_session(
    spec: SigmaMinusNSpec | None = None,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
    *,
    record: bool = False,
    prior_art_status: str = PriorArtStatus.KNOWN.value,
) -> ResearchSession:
    target = spec if spec is not None else map_spec()
    loop = ResearchLoop(ledger if ledger is not None else ResearchLedger())
    return loop.run(
        cast(ProblemSpec, target),
        target.attack_context(),
        corpus,
        prior_art_status=prior_art_status,
        record=record,
    )


def plan_map(
    spec: SigmaMinusNSpec | None = None,
    ledger: ResearchLedger | None = None,
    corpus: ResearchCorpus | None = None,
) -> PlannerReport:
    return plan_map_session(spec, ledger, corpus).attack_report
