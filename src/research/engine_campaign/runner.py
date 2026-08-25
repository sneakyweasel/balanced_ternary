"""Sequential ResearchLoop campaign. No engine attacks are added here."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, cast

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.candidates import score_pool, spec_for_selection
from research.engine_campaign.corpus import seed_baseline_corpus
from research.euclidean_quotient.discovery import seed_complexity_profile as euclidean_profile
from research.euclidean_quotient.planner import plan_euclidean_session
from research.mx_plus_r.discovery import magnitude_census, orbit_of, recurrent_seeds
from research.mx_plus_r.discovery import seed_complexity_profile as mx_profile
from research.mx_plus_r.planner import plan_mx_plus_r_session
from research.mx_plus_r.spec import mx_plus_r_spec, mx_plus_r_step
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop
from research_engine.diagnosis.types import ResearchDecision, SelectionReport
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.report import branch_status_for

FAMILY_PAIRS = ((3, 1), (3, -1), (5, 1), (5, 3), (7, 1))


def _orbit_cyclic(orbit: object, m: int, r: int) -> bool:
    if not isinstance(orbit, tuple) or not orbit:
        return False
    last = orbit[-1]
    if not isinstance(last, int):
        return False
    return mx_plus_r_step(last, m, r) in orbit


@dataclass
class CampaignReport:
    summaries: list[SessionSummary] = field(default_factory=list)
    selection: tuple[SelectionReport, ...] = ()
    target_d_name: str = ""
    target_d_overridden: bool = False
    notes: list[str] = field(default_factory=list)

    def by_target(self, name: str) -> SessionSummary:
        for item in self.summaries:
            if item.target == name:
                return item
        raise KeyError(name)


def _mx_extra(m: int, r: int) -> dict[str, Any]:
    spec = mx_plus_r_spec(m, r)
    profile = mx_profile(spec)
    return {
        "m": m,
        "r": r,
        "magnitude": magnitude_census(m, r),
        "recurrent_seeds": recurrent_seeds(m, r),
        "orbit_27": orbit_of(27, m, r, max_steps=24),
        "orbit_7": orbit_of(7, m, r, max_steps=24),
        "complexity": profile.populated_fields(),
        "layer": "ENGINE REDISCOVERY",
    }


def run_family(corpus: ResearchCorpus, report: CampaignReport) -> None:
    for m, r in FAMILY_PAIRS:
        session = plan_mx_plus_r_session(m, r, corpus=corpus, record=True)
        extra = _mx_extra(m, r)
        extra["role"] = "target_a"
        if (m, r) == (5, 1):
            extra["role"] = "target_a_and_b"
        report.summaries.append(summarize_session(session, extra))


def run_target_b_deep(corpus: ResearchCorpus, report: CampaignReport) -> None:
    """Reuse the (5,1) family session; attach a deeper comparison payload."""

    five = report.by_target("mx_plus_r_5_1")
    three = report.by_target("mx_plus_r_3_1")
    five_three = report.by_target("mx_plus_r_5_3")
    extra = dict(five.extra)
    extra["role"] = "target_b"
    extra["compare_3_1"] = {
            "delta_level": five.delta_level,
            "nearest": five.nearest_target,
            "same_census_kind": five.census_kind == three.census_kind,
            "same_family_coefficients": (
                (five.family or {}).get("p"),
                (five.family or {}).get("r"),
            )
            != (
                (three.family or {}).get("p"),
                (three.family or {}).get("r"),
            ),
            "growth_5_1": (five.extra.get("magnitude") or {}).get("growths"),
            "growth_3_1": (three.extra.get("magnitude") or {}).get("growths"),
            "growth_5_3": (five_three.extra.get("magnitude") or {}).get("growths"),
            "seed_27_orbit": five.extra.get("orbit_27"),
            "seed_7_orbit": five.extra.get("orbit_7"),
            "seed_27_cyclic": _orbit_cyclic(five.extra.get("orbit_27"), 5, 1),
        }
    extra["claim_discipline"] = (
        "growth counts are EMPIRICAL; closure caps are FINITE-HORIZON EXACT; "
        "not divergence and not convergence"
    )
    five.extra.update(extra)


def run_euclidean(corpus: ResearchCorpus, report: CampaignReport) -> None:
    session = plan_euclidean_session(corpus=corpus, record=True)
    skipped = session.attack_report.skipped
    piecewise_skip = next((item for item in skipped if item.attack == "piecewise_affine"), None)
    vector = next((item for item in session.attack_report.results if item.name == "vector_affine"), None)
    extra = {
        "role": "target_c",
        "complexity": euclidean_profile().populated_fields(),
        "piecewise_affine_skipped": None if piecewise_skip is None else piecewise_skip.reason,
        "vector_affine_kind": None if vector is None else vector.evidence.get("census_kind"),
        "missing_structure": (
            "1-D piecewise_affine remains inapplicable; vector_affine is the "
            "generic A_u census"
        ),
        "c1_gated": session.decision is ResearchDecision.ENGINE_LIMITATION,
        "layer": "ENGINE REDISCOVERY",
    }
    if vector is not None:
        extra["vector_consumer"] = "generic vector_affine consumed Euclidean I/O"
    elif session.decision is not ResearchDecision.ENGINE_LIMITATION:
        extra["c1_deferred"] = (
            "C.1 vector census is not built: C.0 did not return ENGINE_LIMITATION. "
            "The missing A_u abstraction is recorded as a best-next-question."
        )
    report.summaries.append(summarize_session(session, extra))
    report.notes.append(
        f"Target C engine decision {session.decision.value}; "
        f"dossier {branch_status_for(session.decision)}"
    )


def run_target_d(corpus: ResearchCorpus, report: CampaignReport) -> None:
    ranking = score_pool(corpus)
    report.selection = ranking
    if not ranking:
        raise RuntimeError("empty Target D pool")
    winner = ranking[0]
    spec = spec_for_selection(winner.name)
    report.target_d_name = winner.name
    report.target_d_overridden = False
    session = ResearchLoop(ResearchLedger()).run(
        spec,
        spec.attack_context(),
        corpus,
        prior_art_status=PriorArtStatus.KNOWN.value,
        record=True,
    )
    extra = {
        "role": "target_d",
        "selection": winner.explanation,
        "selection_value": winner.value,
        "layer": "ENGINE REDISCOVERY",
    }
    report.summaries.append(summarize_session(session, extra))


def run_campaign(corpus: ResearchCorpus | None = None) -> tuple[ResearchCorpus, CampaignReport]:
    memory = corpus if corpus is not None else seed_baseline_corpus()
    report = CampaignReport()
    run_family(memory, report)
    run_target_b_deep(memory, report)
    run_euclidean(memory, report)
    run_target_d(memory, report)
    return memory, report
