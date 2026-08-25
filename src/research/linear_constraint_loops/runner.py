"""Sequential frozen ResearchLoop campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.linear_constraint_loops.candidates import score_pool, spec_for_selection
from research.linear_constraint_loops.discovery import falsify_claims, orbit, quantifier_report
from research.linear_constraint_loops.planner import plan_loop_session
from research.linear_constraint_loops.scout import CARELLI_BASELINE, scout_for
from research.linear_constraint_loops.spec import (
    OneVariableLoopSpec,
    RelationLoopSpec,
    decrement_spec,
    negation_spec,
    rplus_spec,
    sum_strip_spec,
)
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop
from research_engine.diagnosis.types import SelectionReport
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger

TARGETS: tuple[tuple[str, OneVariableLoopSpec], ...] = (
    ("simple_termination", decrement_spec()),
    ("cycle_affine", negation_spec()),
    ("open_strip", rplus_spec()),
)


def _branches(summary: SessionSummary) -> tuple[dict[str, Any], ...]:
    family = summary.family or {}
    extra = summary.extra
    raw = extra.get("branches") or ()
    if raw:
        return tuple(dict(item) for item in raw if isinstance(item, dict))
    if family:
        return (dict(family),)
    return ()


def _structure_origin(name: str, summary: SessionSummary) -> str:
    if name == "slc_rplus":
        branches = _branches(summary)
        if any(int(item.get("q") or 0) == 3 and int(item.get("p") or 0) == 4 for item in branches):
            return "DISCOVERED"
        if summary.census_kind in {"FINITE_CENSUS", "PARAMETERIZED_CENSUS"}:
            return "DISCOVERED"
        return "KNOWN ONLY FROM PRIOR ART"
    if name == "slc_sum_strip":
        if summary.census_kind in {"FINITE_CENSUS", "PARAMETERIZED_CENSUS"}:
            return "DISCOVERED"
        return "GIVEN BY THE ADAPTER"
    if name in {"slc_decrement", "slc_negation", "slc_increment"}:
        return "GIVEN BY THE ADAPTER"
    return "KNOWN ONLY FROM PRIOR ART"


def _yield_report(name: str, summary: SessionSummary, spec: OneVariableLoopSpec | RelationLoopSpec) -> dict[str, Any]:
    origin = _structure_origin(name, summary)
    payload: dict[str, Any] = {
        "Known results rediscovered": (
            f"{origin}; engine decision {summary.decision}; census {summary.census_kind or 'none'}"
        ),
        "New exact identities": (
            summary.strongest_exact or "none beyond the problem definition"
        ),
        "New invariant candidates": "none promoted",
        "New exact invariants": summary.obstruction_scopes or (),
        "New obstructions": summary.obstruction_scopes or (),
        "New conjectures": (
            "none; the open strip question is Carelli Example 4.26"
            if name == "slc_rplus"
            else "none"
        ),
        "New Lean theorems": "Problems.Engine.LinearConstraintLoops (KNOWN identities)",
        "Potentially new mathematics": "none claimed",
        "Engineering changes": 0,
        "structure_origin": origin,
        "scout_open": scout_for(name).open_questions if name in {"slc_decrement", "slc_negation", "slc_rplus", "slc_increment", "slc_sum_strip"} else "",
    }
    if isinstance(spec, RelationLoopSpec):
        payload["quantifiers"] = quantifier_report(spec)
        payload["New counterexamples"] = {}
        payload["termination_class"] = "quantified"
        payload["New existential witnesses"] = payload["quantifiers"]["existential_cycle"]
        payload["New universal statements"] = payload["quantifiers"]["universal_termination"]
    else:
        falsify = falsify_claims(spec)
        payload["falsify"] = falsify
        payload["New counterexamples"] = {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("holds_on_window") is False
        }
        payload["termination_class"] = _termination_class(name, falsify)
    return payload


def _termination_class(name: str, falsify: dict[str, dict[str, object]]) -> str:
    empirical = falsify["empirical_termination"]["holds_on_window"]
    if name == "slc_decrement" and empirical:
        return "universal_termination_theorem"
    if name == "slc_rplus":
        if empirical:
            return "empirical_termination"
        return "open"
    if name in {"slc_negation", "slc_increment"}:
        return "nontermination"
    return "empirical_termination" if empirical else "open"


def _session_extra(role: str, spec: OneVariableLoopSpec | RelationLoopSpec, session_summary_seed: dict[str, Any] | None = None) -> dict[str, Any]:
    extra = {
        "role": role,
        "start": spec.start,
        "legal_at_start": spec.successors(spec.start),
        "control_count_at_start": len(spec.successors(spec.start)),
        "layer": "ENGINE REDISCOVERY",
        "carelli_baseline": tuple(item[0] for item in CARELLI_BASELINE),
    }
    if isinstance(spec, OneVariableLoopSpec):
        extra["orbit_start"] = orbit(spec, spec.start)
    extra.update(session_summary_seed or {})
    return extra


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


def _attach_census_branches(summary: SessionSummary, session) -> None:
    results = {item.name: item for item in session.attack_report.results}
    census = results.get("piecewise_affine")
    if census is None:
        return
    raw = census.evidence.get("branches") or ()
    summary.extra["branches"] = tuple(dict(item) for item in raw if isinstance(item, dict))
    summary.extra["latent_controls"] = census.evidence.get("latent_controls") or ()
    summary.extra["unresolved"] = census.evidence.get("unresolved") or ()


def run_first_batch(corpus: ResearchCorpus, report: CampaignReport) -> None:
    for role, spec in TARGETS:
        session = plan_loop_session(spec, corpus=corpus, record=True)
        extra = _session_extra(role, spec)
        summary = summarize_session(session, extra)
        _attach_census_branches(summary, session)
        summary.extra["yield"] = _yield_report(spec.name, summary, spec)
        report.summaries.append(summary)
        report.notes.append(
            f"{spec.name}: origin={summary.extra['yield']['structure_origin']} "
            f"decision={summary.decision} census={summary.census_kind or 'none'}"
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


def run_nondeterministic_target(corpus: ResearchCorpus, report: CampaignReport) -> None:
    spec = sum_strip_spec()
    session = plan_loop_session(spec, corpus=corpus, record=True)
    extra = _session_extra("nondeterministic_slc", spec)
    extra["piecewise_affine_applicable"] = "piecewise_affine" not in {
        item.attack for item in session.attack_report.skipped
    }
    extra["quantifiers"] = quantifier_report(spec)
    summary = summarize_session(session, extra)
    _attach_census_branches(summary, session)
    summary.extra["yield"] = _yield_report(spec.name, summary, spec)
    fp = session.diagnosis.fingerprint
    summary.extra["control_structure"] = fp.control_structure
    summary.extra["transition_architecture"] = fp.transition_architecture
    report.summaries.append(summary)
    report.notes.append(
        f"{spec.name}: control={fp.control_structure} census={summary.census_kind or 'none'} "
        f"decision={summary.decision} skipped={summary.skipped}"
    )


def run_campaign(corpus: ResearchCorpus | None = None) -> tuple[ResearchCorpus, CampaignReport]:
    memory = corpus if corpus is not None else seed_baseline_corpus()
    report = CampaignReport()
    run_first_batch(memory, report)
    run_next_selection(memory, report)
    run_nondeterministic_target(memory, report)
    return memory, report
