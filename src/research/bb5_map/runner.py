"""Sequential frozen ResearchLoop campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.bb5_map.discovery import falsify_claims, orbit
from research.bb5_map.planner import plan_map_session
from research.bb5_map.scout import BASELINE, scout_for
from research.bb5_map.spec import PartialFiveThreeSpec, map_spec
from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research_engine.diagnosis.corpus import ResearchCorpus


def _branches(summary: SessionSummary) -> tuple[dict[str, Any], ...]:
    extra = summary.extra
    raw = extra.get("branches") or ()
    if raw:
        return tuple(dict(item) for item in raw if isinstance(item, dict))
    if summary.family:
        return (dict(summary.family),)
    return ()


def _structure_origin(summary: SessionSummary) -> str:
    branches = _branches(summary)
    if any(int(item.get("q") or 0) == 3 and int(item.get("p") or 0) == 5 for item in branches):
        return "DISCOVERED"
    if summary.census_kind in {"FINITE_CENSUS", "PARAMETERIZED_CENSUS"}:
        return "DISCOVERED"
    return "KNOWN ONLY FROM PRIOR ART"


def _yield_report(summary: SessionSummary, spec: PartialFiveThreeSpec) -> dict[str, Any]:
    origin = _structure_origin(summary)
    falsify = falsify_claims(spec)
    empirical = falsify["empirical_termination"]["holds_on_window"]
    return {
        "Known results rediscovered": (
            f"{origin}; engine decision {summary.decision}; census {summary.census_kind or 'none'}"
        ),
        "New exact identities": summary.strongest_exact or "none beyond the problem definition",
        "New branch/domain certificates": summary.domain_direction or "",
        "New cycle obstructions": summary.obstruction_scopes or (),
        "New terminal/reachability obstructions": summary.obstruction_scopes or (),
        "New counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("holds_on_window") is False
        },
        "New conjectures": "none; universal convergence of the map on N is literature-open",
        "New Lean theorems": "Problems.Engine.BB5Map (KNOWN identities)",
        "Potentially new mathematics": "none claimed",
        "Engineering changes": 0,
        "structure_origin": origin,
        "falsify": falsify,
        "termination_class": (
            "empirical_termination_on_window" if empirical else "open"
        ),
        "scout_open": scout_for(spec.name).open_questions,
    }


def _attach_census_branches(summary: SessionSummary, session) -> None:
    results = {item.name: item for item in session.attack_report.results}
    census = results.get("piecewise_affine")
    if census is None:
        return
    raw = census.evidence.get("branches") or ()
    summary.extra["branches"] = tuple(dict(item) for item in raw if isinstance(item, dict))
    summary.extra["latent_controls"] = census.evidence.get("latent_controls") or ()
    summary.extra["unresolved"] = census.evidence.get("unresolved") or ()
    summary.extra["census_kind"] = census.evidence.get("census_kind")
    domain = results.get("parameter_domain")
    if domain is not None:
        summary.extra["domains"] = domain.evidence.get("domains") or ()
        summary.extra["domain_claim"] = domain.claim
    words = results.get("control_word")
    if words is not None:
        summary.extra["control_word_claim"] = words.claim
        summary.extra["word_count"] = words.evidence.get("word_count") or words.evidence.get("count")
    obstructed = results.get("control_obstruction")
    if obstructed is not None:
        summary.extra["obstruction_claim"] = obstructed.claim
        summary.extra["obstruction_certificates"] = obstructed.evidence.get("certificates") or ()


@dataclass
class CampaignReport:
    summaries: list[SessionSummary] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def by_target(self, name: str) -> SessionSummary:
        for item in self.summaries:
            if item.target == name:
                return item
        raise KeyError(name)


def run_campaign(corpus: ResearchCorpus | None = None) -> tuple[ResearchCorpus, CampaignReport]:
    memory = corpus if corpus is not None else seed_baseline_corpus()
    report = CampaignReport()
    spec = map_spec()
    session = plan_map_session(spec, corpus=memory, record=True)
    extra = {
        "role": "blind_map",
        "start": spec.start,
        "legal_at_start": spec.successors(spec.start),
        "orbit_start": orbit(spec, spec.start),
        "layer": "ENGINE REDISCOVERY",
        "baseline": tuple(item[0] for item in BASELINE),
    }
    summary = summarize_session(session, extra)
    _attach_census_branches(summary, session)
    fp = session.diagnosis.fingerprint
    summary.extra["control_structure"] = fp.control_structure
    summary.extra["transition_architecture"] = fp.transition_architecture
    summary.extra["yield"] = _yield_report(summary, spec)
    report.summaries.append(summary)
    report.notes.append(
        f"{spec.name}: origin={summary.extra['yield']['structure_origin']} "
        f"decision={summary.decision} census={summary.census_kind or 'none'} "
        f"skipped={summary.skipped}"
    )
    return memory, report
