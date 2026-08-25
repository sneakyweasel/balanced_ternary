"""Frozen ResearchLoop campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.switching_affine_z2_origin.discovery import evidence_state, falsify_claims
from research.switching_affine_z2_origin.planner import plan_map_session
from research.switching_affine_z2_origin.scout import BASELINE
from research.switching_affine_z2_origin.spec import TwoPathZ2Spec, map_spec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.memory.board import assemble_board
from research_engine.memory.ingest import experiment_from_session
from research_engine.memory.seed_records import historical_experiments
from research_engine.memory.store import ResearchMemory
from research_engine.memory.types import (
    GreyLoot,
    GreyLootKind,
    LootEvidence,
    MathematicalYield,
    NoveltyLevel,
    NoveltyStatus,
    PriorArtMemory,
    ScoutDossier,
)
from research_engine.planner.hypothesis import PriorArtStatus

CURRENT = "switching_affine_z2_origin"


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


def _planner_signature(session) -> tuple[tuple[str, str, str], ...]:
    results = tuple((item.name, item.status.value, item.claim) for item in session.attack_report.results)
    skipped = tuple((item.attack, item.reason) for item in session.attack_report.skipped)
    return results + skipped


def _attach_census(summary: SessionSummary, session) -> None:
    results = {item.name: item for item in session.attack_report.results}
    census = results.get("vector_affine") or results.get("piecewise_affine")
    if census is not None:
        summary.extra["census_kind"] = census.evidence.get("census_kind")
        summary.extra["branches"] = tuple(
            dict(item) for item in (census.evidence.get("branches") or ()) if isinstance(item, dict)
        )
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
        summary.extra["closure_origin"] = any(
            isinstance(state, tuple) and tuple(int(part) for part in state) == (0, 0) for state in union
        )
    obstructed = results.get("control_obstruction")
    if obstructed is not None:
        summary.extra["obstruction_claim"] = obstructed.claim
        summary.extra["obstruction_status"] = obstructed.status.value


def _yield_report(summary: SessionSummary, spec: TwoPathZ2Spec) -> dict[str, Any]:
    evidence = evidence_state(spec)
    falsify = falsify_claims(spec)
    return {
        "known_rediscoveries": (
            f"engine decision {summary.decision}; census {summary.census_kind or 'none'}"
        ),
        "new_exact_results": summary.strongest_exact or "definition identities",
        "new_invariants": "nonnegative orthant closed; unique origin preimages off N^2",
        "new_obstructions": "N^2 \\ {(0,0)} cannot reach (0,0) in one step, hence never",
        "new_origin_reachability_results": evidence["origin_at"],
        "new_nonreachability_results": "(3,2) does not reach (0,0) on the bound; N^2 class",
        "new_quotients": "none promoted",
        "new_control_constraints": "singleton dummy control only",
        "new_counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "new_conjectures": "none",
        "new_formalizations": "Problems.Engine.TwoPathZ2",
        "potentially_new_mathematics": "none claimed",
        "unresolved_questions": "universal termination on all of Z^2",
        "engineering_changes": 0,
        "evidence": evidence,
        "falsify": falsify,
    }


@dataclass
class CampaignReport:
    summaries: list[SessionSummary] = field(default_factory=list)
    next_target_name: str = ""
    next_target_overridden: bool = False
    notes: list[str] = field(default_factory=list)
    memory: ResearchMemory | None = None
    planner_unchanged_with_memory: bool = False
    next_ev: tuple[tuple[str, float], ...] = ()
    failure_learning_note: str = ""

    def by_target(self, name: str) -> SessionSummary:
        for item in self.summaries:
            if item.target == name:
                return item
        raise KeyError(name)


def run_campaign(corpus: ResearchCorpus | None = None) -> tuple[ResearchCorpus, CampaignReport]:
    memory_corpus = corpus if corpus is not None else seed_baseline_corpus()
    store = ResearchMemory(historical_experiments())
    spec = map_spec()
    plain = plan_map_session(spec, corpus=memory_corpus, record=False)
    probe = ResearchMemory()
    session = plan_map_session(
        spec,
        corpus=memory_corpus,
        record=True,
        memory=probe,
        prior_art_status=PriorArtStatus.KNOWN.value,
    )
    unchanged = _planner_signature(plain) == _planner_signature(session)
    extra = {
        "computation_exhausted": False,
        "infinite_reachability_unresolved": False,
        "representation_novelty": NoveltyLevel.MEDIUM.value,
        "mathematical_novelty": NoveltyLevel.NONE.value,
        "novelty_status": NoveltyStatus.KNOWN_REDISCOVERY.value,
        "engineering_changes": 0,
        "mathematical_yield": MathematicalYield(
            known_rediscoveries=("two-path integer loop from the stored blind packet",),
            new_exact_results=("origin preimages; unit 2-cycle; N^2 one-step avoidance",),
            new_formalizations=("Problems.Engine.TwoPathZ2",),
            new_obstructions=("nonnegative non-origin states never map to origin",),
            unresolved_questions=("termination on all of Z^2",),
            engineering_changes=0,
        ),
        "grey_loot": (
            GreyLoot(
                id="two_path_z2:loot:cycle",
                kind=GreyLootKind.COUNTEREXAMPLE,
                statement="unit pair (1,0)<->(0,1) is a 2-cycle that never hits (0,0)",
                evidence=LootEvidence.PROVED,
                experiment_id="two_path_z2",
                target="two_path_z2",
            ),
            GreyLoot(
                id="two_path_z2:loot:n2",
                kind=GreyLootKind.CANDIDATE_INVARIANT,
                statement="N^2 is invariant and (0,0) has no other nonnegative preimage",
                evidence=LootEvidence.PROVED,
                experiment_id="two_path_z2",
                target="two_path_z2",
            ),
        ),
    }
    experiment = experiment_from_session(
        session,
        spec,
        spec.attack_context(),
        experiment_id="two_path_z2",
        target_family="switching_affine",
        extra=extra,
        scout=ScoutDossier(
            target="two_path_z2",
            problem_definition=(
                "On the declared two-path integer map, is (0,0) reachable from (3,2)?"
            ),
            literature=(
                "ben-amram-genaim-ouaknine-worrell-2025-termination-survey",
                "hosseini-ouaknine-worrell-2019-termination-linear-loops",
            ),
        ),
        prior_art=PriorArtMemory(
            literature_ids=(
                "ben-amram-genaim-ouaknine-worrell-2025-termination-survey",
                "hosseini-ouaknine-worrell-2019-termination-linear-loops",
            ),
            independently_rediscovered=False,
            known_theorem_status="KNOWN",
        ),
    )
    store.add(experiment)
    store.finalize("two_path_z2")
    payload = {
        "role": "flagship",
        "attack_table": _attack_table(session),
        "layer": "ENGINE REDISCOVERY",
        "baseline": tuple(item[0] for item in BASELINE),
        "failure_classes": tuple(item.failure_class.value for item in experiment.failures),
        "planner_unchanged_with_memory": unchanged,
    }
    summary = summarize_session(session, payload)
    _attach_census(summary, session)
    fp = session.diagnosis.fingerprint
    summary.extra["control_structure"] = fp.control_structure
    summary.extra["numerical_contraction"] = fp.numerical_contraction
    summary.extra["eventual_region"] = fp.eventual_region
    summary.extra["piecewise_affine_structure"] = fp.piecewise_affine_structure
    summary.extra["affine_control_type"] = fp.affine_control_type
    summary.extra["yield"] = _yield_report(summary, spec)
    board = assemble_board(store, memory_corpus)
    leftovers = [
        item
        for item in board.targets
        if not item.already_run and item.name != CURRENT
    ]
    leftovers.sort(key=lambda item: (-item.expected_research_value.value, item.name))
    pick = leftovers[0] if leftovers else None
    report = CampaignReport(
        summaries=[summary],
        memory=store,
        planner_unchanged_with_memory=unchanged,
        next_target_name=pick.name if pick is not None else "",
        next_target_overridden=False,
        next_ev=tuple((item.name, item.expected_research_value.value) for item in leftovers[:5]),
        failure_learning_note=pick.expected_research_value.reason if pick is not None else "",
    )
    report.notes.append(
        f"{spec.name}: decision={summary.decision} census={summary.census_kind or 'none'} "
        f"unchanged={unchanged} next={report.next_target_name}"
    )
    return memory_corpus, report
