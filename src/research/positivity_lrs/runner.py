"""Sequential frozen ResearchLoop campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.positivity_lrs.candidates import score_pool, spec_for_selection
from research.positivity_lrs.discovery import evidence_state, falsify_claims
from research.positivity_lrs.planner import plan_map_session
from research.positivity_lrs.scout import BASELINE
from research.positivity_lrs.spec import CATALOG, CompanionObsSpec, skip_attacks_for_dimension
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop
from research_engine.diagnosis.types import SelectionReport
from research_engine.memory.ingest import experiment_from_session
from research_engine.memory.seed_records import historical_experiments
from research_engine.memory.store import ResearchMemory
from research_engine.memory.types import (
    FailureClass,
    FailureRecord,
    GreyLoot,
    GreyLootKind,
    ImportanceLevel,
    LootEvidence,
    MathematicalYield,
    NoveltyLevel,
    NoveltyStatus,
)
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.ledger import ResearchLedger

TARGETS: tuple[tuple[str, str], ...] = (
    ("trivially_nonneg", "companion_obs_nonneg_small"),
    ("early_negative", "companion_obs_early_negative"),
    ("periodic_sign", "companion_obs_periodic_sign"),
    ("finite_negative", "companion_obs_finite_negative"),
    ("order3_classified", "companion_obs_order3"),
    ("open_flagship", "companion_obs_order10"),
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


def _yield_report(summary: SessionSummary, spec: CompanionObsSpec) -> dict[str, Any]:
    evidence = evidence_state(spec)
    falsify = falsify_claims(spec)
    return {
        "Known rediscoveries": (
            f"engine decision {summary.decision}; census {summary.census_kind or 'none'}"
        ),
        "New exact identities": summary.strongest_exact or "none beyond the problem definition",
        "New invariants": "none promoted",
        "New modular exclusions": "none; residues are not a sign theorem",
        "New negative witnesses": evidence["first_negative"],
        "New counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "New conjectures": "none; a nonnegative window is not restated as a law",
        "New reductions": "none",
        "Lean-certified results": "Problems.Engine.CompanionObservation (KNOWN identities)",
        "Potentially new mathematics": "none claimed",
        "Unresolved bottlenecks": (
            "first-coordinate nonnegativity for all indices"
            if evidence["first_negative"] is None
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
        summary.extra["closure_negative"] = any(
            isinstance(state, tuple) and state and int(state[0]) < 0 for state in union
        )


def _flagship_extra(spec: CompanionObsSpec, evidence: dict[str, object]) -> dict[str, Any]:
    exhausted = bool(evidence.get("exhausted")) or bool(skip_attacks_for_dimension(spec.dimension))
    return {
        "computation_exhausted": exhausted,
        "infinite_reachability_unresolved": evidence.get("first_negative") is None,
        "representation_novelty": NoveltyLevel.LOW.value,
        "mathematical_novelty": NoveltyLevel.NONE.value,
        "novelty_status": NoveltyStatus.KNOWN_REDISCOVERY.value,
        "engineering_changes": 0,
        "mathematical_yield": MathematicalYield(
            known_rediscoveries=("order-10 companion window of Bacik et al. 2026 survey (16)",),
            unresolved_questions=("whether survey sequence (16) is nonnegative for every n",),
            engineering_changes=0,
        ),
        "grey_loot": (
            GreyLoot(
                id=f"{spec.name}:loot:budget",
                kind=GreyLootKind.COMPUTATIONAL_BOTTLENECK,
                statement="vector census 25^10 exceeds 50000 cells",
                evidence=LootEvidence.FINITE_RANGE,
                experiment_id=spec.name,
                target=spec.name,
                failure_class=FailureClass.COMPUTATIONAL,
                bottleneck="finite_budget_exhausted",
            ),
            GreyLoot(
                id=f"{spec.name}:loot:global",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement=(
                    "finite nonnegative prefix does not decide infinite-horizon "
                    "first-coordinate nonnegativity"
                ),
                evidence=LootEvidence.OBSERVED,
                experiment_id=spec.name,
                target=spec.name,
                failure_class=FailureClass.GLOBAL_REASONING,
                bottleneck="finite_to_infinite_certificate",
                reusable_lesson=(
                    "Skolem hyperplane reachability and half-space safety fail for "
                    "the same finite-to-infinite gap on companion-matrix dynamics."
                ),
            ),
        ),
        "failures": (
            FailureRecord(
                id=f"{spec.name}:global",
                target=spec.name,
                experiment_id=spec.name,
                engine_version="0.2.2",
                phase="reachability",
                attack="closure",
                failure_class=FailureClass.GLOBAL_REASONING,
                representation_status="LANGUAGE_ADEQUATE",
                mathematical_bottleneck="finite_to_infinite_certificate",
                evidence="companion window fits; infinite-horizon nonnegativity unresolved",
                reusable_lesson=(
                    "Changing existential hyperplane reachability into universal "
                    "half-space safety does not create a new frozen-engine capability."
                ),
                engineering_action="PARK",
                research_value=ImportanceLevel.HIGH,
                affected_attack_family="global_reachability",
            ),
            FailureRecord(
                id=f"{spec.name}:computational",
                target=spec.name,
                experiment_id=spec.name,
                engine_version="0.2.2",
                phase="census",
                attack="vector_affine",
                failure_class=FailureClass.COMPUTATIONAL,
                representation_status="VECTOR_AFFINE_ADEQUATE",
                mathematical_bottleneck="finite_budget_exhausted",
                evidence="25^10 census cube skipped; COMPUTATION_EXHAUSTED",
                reusable_lesson="Computational blockage is not mathematical impossibility.",
                affected_attack_family="vector_census",
            ),
        ),
    }


@dataclass
class CampaignReport:
    summaries: list[SessionSummary] = field(default_factory=list)
    selection: tuple[SelectionReport, ...] = ()
    next_target_name: str = ""
    next_target_overridden: bool = False
    notes: list[str] = field(default_factory=list)
    memory: ResearchMemory | None = None
    clusters: tuple[str, ...] = ()
    next_ev: tuple[tuple[str, float], ...] = ()

    def by_target(self, name: str) -> SessionSummary:
        for item in self.summaries:
            if item.target == name:
                return item
        raise KeyError(name)


def run_portfolio(corpus: ResearchCorpus, report: CampaignReport, store: ResearchMemory) -> None:
    for role, name in TARGETS:
        spec = CATALOG[name]
        extra_ingest: dict[str, Any] = {}
        if role == "open_flagship":
            extra_ingest = _flagship_extra(spec, evidence_state(spec))
        session = plan_map_session(spec, corpus=corpus, record=True)
        experiment = experiment_from_session(
            session,
            spec,
            spec.attack_context(),
            experiment_id=spec.name,
            target_family="linear_recurrence",
            extra=extra_ingest,
        )
        store.add(experiment)
        store.finalize(spec.name)
        extra = {
            "role": role,
            "dimension": spec.dimension,
            "window": spec.window,
            "attack_table": _attack_table(session),
            "layer": "ENGINE REDISCOVERY",
            "baseline": tuple(item[0] for item in BASELINE),
            "skip_attacks": skip_attacks_for_dimension(spec.dimension),
            "failure_classes": tuple(item.failure_class.value for item in experiment.failures),
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


def run_next_selection(corpus: ResearchCorpus, report: CampaignReport, store: ResearchMemory) -> None:
    ranking = score_pool(corpus, memory=store)
    report.selection = ranking
    report.next_ev = tuple((item.name, item.value) for item in ranking)
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
        memory=store,
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
    store = ResearchMemory(historical_experiments())
    report = CampaignReport(memory=store)
    run_portfolio(memory, report, store)
    run_next_selection(memory, report, store)
    report.clusters = tuple(item.id for item in store.clusters())
    return memory, report
