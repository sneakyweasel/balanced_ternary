"""Sequential frozen ResearchLoop campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.aliquot_dynamics.candidates import score_pool, spec_for_selection
from research.aliquot_dynamics.discovery import falsify_claims, orbit
from research.aliquot_dynamics.planner import plan_map_session
from research.aliquot_dynamics.scout import BASELINE
from research.aliquot_dynamics.spec import (
    TRANSITION_UNRESOLVED,
    SigmaMinusNSpec,
    map_spec,
    transition_status,
)
from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop
from research_engine.diagnosis.types import SelectionReport
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger

TARGETS: tuple[tuple[str, int], ...] = (
    ("known_termination", 12),
    ("known_fixed_point", 6),
    ("known_period_two", 220),
    ("open_flagship", 276),
)


def _attack_table(session) -> dict[str, str]:
    table: dict[str, str] = {}
    for item in session.attack_report.skipped:
        reason = item.reason.lower()
        table[item.attack] = "INAPPLICABLE" if ("inapplicable" in reason or "needs" in reason) else "SKIPPED"
    for item in session.attack_report.results:
        table[item.name] = item.status.value
    return table


def _yield_report(summary: SessionSummary, spec: SigmaMinusNSpec) -> dict[str, Any]:
    falsify = falsify_claims(spec)
    start_orbit = orbit(spec, spec.start)
    return {
        "Known rediscoveries": (
            f"engine decision {summary.decision}; census {summary.census_kind or 'none'}"
        ),
        "New exact identities": summary.strongest_exact or "none beyond the problem definition",
        "New invariants": "none promoted",
        "New obstructions": summary.obstruction_scopes or (),
        "New counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("holds_on_window") is False
        },
        "New trajectory classifications": start_orbit.get("kind"),
        "New conjectures": "none; Catalan–Dickson is not restated",
        "Lean-certified results": "Problems.Engine.AliquotDynamics (KNOWN identities)",
        "Potentially new mathematics": "none claimed",
        "Unresolved questions": "fate of seed 276" if spec.start == 276 else "",
        "Engineering changes": 0,
        "falsify": falsify,
        "start_orbit": start_orbit,
        "start_status": transition_status(spec.start),
    }


def _attach_census(summary: SessionSummary, session) -> None:
    results = {item.name: item for item in session.attack_report.results}
    census = results.get("piecewise_affine")
    if census is not None:
        summary.extra["census_kind"] = census.evidence.get("census_kind")
        summary.extra["branches"] = tuple(
            dict(item) for item in (census.evidence.get("branches") or ()) if isinstance(item, dict)
        )
        summary.extra["unresolved"] = census.evidence.get("unresolved") or ()
    closure = results.get("closure")
    if closure is not None:
        summary.extra["closure_complete"] = closure.evidence.get("complete")
        summary.extra["closure_size"] = closure.evidence.get("union_size")


@dataclass
class CampaignReport:
    summaries: list[SessionSummary] = field(default_factory=list)
    selection: tuple[SelectionReport, ...] = ()
    next_target_name: str = ""
    next_target_overridden: bool = False
    notes: list[str] = field(default_factory=list)

    def by_target(self, name: str) -> SessionSummary:
        for item in self.summaries:
            if item.target == name:
                return item
        raise KeyError(name)


def run_portfolio(corpus: ResearchCorpus, report: CampaignReport) -> None:
    for role, start in TARGETS:
        spec = map_spec(start=start)
        session = plan_map_session(spec, corpus=corpus, record=True)
        extra = {
            "role": role,
            "start": start,
            "legal_at_start": spec.successors(spec.start),
            "start_status": transition_status(spec.start),
            "attack_table": _attack_table(session),
            "layer": "ENGINE REDISCOVERY",
            "baseline": tuple(item[0] for item in BASELINE),
        }
        if extra["start_status"] == TRANSITION_UNRESOLVED:
            extra["transition"] = TRANSITION_UNRESOLVED
        summary = summarize_session(session, extra)
        _attach_census(summary, session)
        fp = session.diagnosis.fingerprint
        summary.extra["control_structure"] = fp.control_structure
        summary.extra["numerical_contraction"] = fp.numerical_contraction
        summary.extra["eventual_region"] = fp.eventual_region
        summary.extra["piecewise_affine_structure"] = fp.piecewise_affine_structure
        summary.extra["yield"] = _yield_report(summary, spec)
        report.summaries.append(summary)
        report.notes.append(
            f"{spec.name}: role={role} decision={summary.decision} "
            f"census={summary.census_kind or 'none'} class={summary.semantic_class}"
        )


def run_next_selection(corpus: ResearchCorpus, report: CampaignReport) -> None:
    ranking = score_pool(corpus)
    report.selection = ranking
    if not ranking:
        raise RuntimeError("empty ResearchLoop pool")
    winner = ranking[0]
    spec = spec_for_selection(winner.name)
    report.next_target_name = winner.name
    report.next_target_overridden = False
    session = ResearchLoop(ResearchLedger()).run(
        spec,
        spec.attack_context(),
        corpus,
        prior_art_status=PriorArtStatus.KNOWN.value,
        record=True,
    )
    extra = {
        "role": "researchloop_next",
        "selection": winner.explanation,
        "selection_value": winner.value,
        "layer": "ENGINE REDISCOVERY",
    }
    report.summaries.append(summarize_session(session, extra))
    report.notes.append(
        f"ResearchLoop selected {winner.name} with ExpectedResearchValue={winner.value:.3f}"
    )


def run_campaign(corpus: ResearchCorpus | None = None) -> tuple[ResearchCorpus, CampaignReport]:
    memory = corpus if corpus is not None else seed_baseline_corpus()
    report = CampaignReport()
    run_portfolio(memory, report)
    run_next_selection(memory, report)
    return memory, report
