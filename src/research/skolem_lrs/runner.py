"""Sequential frozen ResearchLoop campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.skolem_lrs.candidates import score_pool, spec_for_selection
from research.skolem_lrs.discovery import evidence_state, falsify_claims
from research.skolem_lrs.planner import plan_map_session
from research.skolem_lrs.scout import BASELINE
from research.skolem_lrs.spec import CATALOG, CompanionShiftSpec, skip_attacks_for_dimension
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop
from research_engine.diagnosis.types import SelectionReport
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger

TARGETS: tuple[tuple[str, str], ...] = (
    ("trivial_zero", "companion_shift_zero_small"),
    ("zero_free_positive", "companion_shift_positive"),
    ("periodic_zero", "companion_shift_periodic"),
    ("order3_classified", "companion_shift_order3"),
    ("open_flagship", "companion_shift_order6"),
)


def _attack_table(session) -> dict[str, str]:
    table: dict[str, str] = {}
    for item in session.attack_report.skipped:
        reason = item.reason.lower()
        if "skipped by adapter" in reason:
            table[item.attack] = "COMPUTATION_EXHAUSTED"
        elif "inapplicable" in reason or "needs" in reason:
            table[item.attack] = "INAPPLICABLE"
        else:
            table[item.attack] = "SKIPPED"
    for item in session.attack_report.results:
        table[item.name] = item.status.value
    return table


def _yield_report(summary: SessionSummary, spec: CompanionShiftSpec) -> dict[str, Any]:
    evidence = evidence_state(spec)
    falsify = falsify_claims(spec)
    return {
        "Known rediscoveries": (
            f"engine decision {summary.decision}; census {summary.census_kind or 'none'}"
        ),
        "New exact identities": summary.strongest_exact or "none beyond the problem definition",
        "New invariants": "none promoted",
        "New modular exclusions": (
            "none; prefix residue gaps are not integer exclusion"
            if evidence["moduli_without_zero"]
            else "none"
        ),
        "New zero witnesses": evidence["zero_at"],
        "New counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "New conjectures": "none; unbounded vanishing is not restated",
        "New reductions": "none",
        "Lean-certified results": "Problems.Engine.CompanionShift (KNOWN identities)",
        "Potentially new mathematics": "none claimed",
        "Unresolved bottlenecks": (
            "first-coordinate vanishing for all indices"
            if evidence["zero_at"] is None
            else ""
        ),
        "Engineering changes": 0,
        "evidence": evidence,
        "falsify": falsify,
        "skip_attacks": skip_attacks_for_dimension(spec.dimension),
    }


def _attach_census(summary: SessionSummary, session) -> None:
    results = {item.name: item for item in session.attack_report.results}
    census = results.get("vector_affine") or results.get("piecewise_affine")
    if census is not None:
        summary.extra["census_kind"] = census.evidence.get("census_kind")
        summary.extra["branches"] = tuple(
            dict(item) for item in (census.evidence.get("branches") or ()) if isinstance(item, dict)
        )
        summary.extra["unresolved"] = census.evidence.get("unresolved") or ()
        if census.evidence.get("branches"):
            first = census.evidence["branches"][0]
            if isinstance(first, dict):
                summary.extra["recovered_matrix"] = first.get("matrix")
                summary.extra["recovered_offset"] = first.get("offset")
    closure = results.get("closure")
    if closure is not None:
        summary.extra["closure_complete"] = closure.evidence.get("complete")
        summary.extra["closure_size"] = closure.evidence.get("union_size")
        union = closure.evidence.get("union") or ()
        summary.extra["closure_zero"] = any(
            isinstance(state, tuple) and state and int(state[0]) == 0 for state in union
        )


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
    for role, name in TARGETS:
        spec = CATALOG[name]
        session = plan_map_session(spec, corpus=corpus, record=True)
        extra = {
            "role": role,
            "dimension": spec.dimension,
            "window": spec.window,
            "attack_table": _attack_table(session),
            "layer": "ENGINE REDISCOVERY",
            "baseline": tuple(item[0] for item in BASELINE),
            "skip_attacks": skip_attacks_for_dimension(spec.dimension),
        }
        summary = summarize_session(session, extra)
        _attach_census(summary, session)
        fp = session.diagnosis.fingerprint
        summary.extra["control_structure"] = fp.control_structure
        summary.extra["numerical_contraction"] = fp.numerical_contraction
        summary.extra["eventual_region"] = fp.eventual_region
        summary.extra["piecewise_affine_structure"] = fp.piecewise_affine_structure
        summary.extra["affine_control_type"] = fp.affine_control_type
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
