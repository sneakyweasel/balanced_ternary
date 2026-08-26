"""Frozen ResearchLoop / StrategyPlanner campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.reverse_and_add_base3.discovery import evidence_state, falsify_claims
from research.reverse_and_add_base3.planner import plan_map_session, plan_strategy
from research.reverse_and_add_base3.scout import BASELINE
from research.reverse_and_add_base3.spec import ReverseAddSpec, map_spec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.memory.board import assemble_board
from research_engine.memory.ingest import experiment_from_session
from research_engine.memory.seed_records import historical_experiments
from research_engine.memory.store import ResearchMemory
from research_engine.memory.types import (
    FailureClass,
    FailureRecord,
    FailureStatus,
    GreyLoot,
    GreyLootKind,
    ImportanceLevel,
    LootEvidence,
    MathematicalYield,
    NoveltyLevel,
    NoveltyStatus,
    PriorArtMemory,
    ScoutDossier,
)
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.strategy import ResearchGoal

CURRENT = "reverse_and_add_base3"
LIVE_ID = "reverse_add_bt"


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
    table = _attack_table(session)
    summary.extra["piecewise_affine_status"] = table.get("piecewise_affine", "")
    summary.extra["closure_status"] = table.get("closure", "")
    results = {item.name: item for item in session.attack_report.results}
    census = results.get("piecewise_affine")
    if census is not None:
        summary.extra["census_kind"] = census.evidence.get("census_kind")
    closure = results.get("closure")
    if closure is not None:
        summary.extra["closure_complete"] = closure.evidence.get("complete")
        summary.extra["closure_size"] = closure.evidence.get("union_size")


def _yield_report(summary: SessionSummary, spec: ReverseAddSpec) -> dict[str, Any]:
    evidence = evidence_state(spec)
    falsify = falsify_claims(spec)
    return {
        "known_rediscoveries": (
            f"engine decision {summary.decision}; piecewise {summary.extra.get('piecewise_affine_status')}"
        ),
        "new_exact_results": "T(0)=0; packet seed 196 reaches 0 in eight steps",
        "new_invariants": "none; finite seed closure is not a Z-theorem",
        "new_obstructions": "none; no residue-affine cover",
        "new_origin_reachability_results": evidence["steps_to_zero"],
        "new_nonreachability_results": "none claimed on integers",
        "new_quotients": "none promoted",
        "new_control_constraints": "singleton dummy control only",
        "new_counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "new_conjectures": "none",
        "new_formalizations": "Problems.Engine.ReverseAdd",
        "potentially_new_mathematics": "none claimed",
        "unresolved_questions": "whether every integer seed hits a reverse-fixed point",
        "engineering_changes": 0,
        "evidence": evidence,
        "falsify": falsify,
    }


def _representation_failure() -> FailureRecord:
    return FailureRecord(
        id="reverse_add_bt:representation",
        target="reverse_add_bt",
        experiment_id="reverse_and_add_base3",
        engine_version="0.2.1",
        phase="census",
        attack="piecewise_affine",
        failure_class=FailureClass.REPRESENTATION,
        representation_status="NON_AFFINE",
        mathematical_bottleneck="outside_affine_valuation_control",
        evidence="digit reverse-plus-add has no complete piecewise-affine cover on the sample window",
        reusable_lesson=(
            "Digit reverse-plus-add is outside residue-affine language; a finite "
            "seed-196 closure is not digit-fold saturation, not aliquot truncation, "
            "and not a Z-theorem."
        ),
        prior_art_status="KNOWN",
        engineering_action="PARK",
        research_value=ImportanceLevel.HIGH,
        status=FailureStatus.PARKED,
        affected_attack_family="latent_affine",
        minimal_example="n |-> n + digit_reverse(n)",
    )


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
    strategy_chain: str = ""

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
    blind_strategy = plan_strategy(spec, goal=ResearchGoal.TERMINATION, memory=None)
    extra = {
        "computation_exhausted": False,
        "infinite_reachability_unresolved": False,
        "representation_novelty": NoveltyLevel.MEDIUM.value,
        "mathematical_novelty": NoveltyLevel.NONE.value,
        "novelty_status": NoveltyStatus.KNOWN_REDISCOVERY.value,
        "engineering_changes": 0,
        "failures": (_representation_failure(),),
        "mathematical_yield": MathematicalYield(
            known_rediscoveries=(
                "packet seed 196 reaches 0 in eight steps",
                "no complete piecewise-affine cover",
            ),
            new_exact_results=("T(0)=0", "196 maps to 392 then reaches 0"),
            new_formalizations=("Problems.Engine.ReverseAdd",),
            new_obstructions=("none; finite seed closure is not a reverse-fixed theorem",),
            new_counterexamples=("T(196)=392 is not digit-sum or aliquot; T(8)=0 is not the floor-power map",),
            unresolved_questions=("whether every integer seed hits a reverse-fixed point",),
            engineering_changes=0,
        ),
        "grey_loot": (
            GreyLoot(
                id="reverse_add_bt:loot:mismatch",
                kind=GreyLootKind.REPRESENTATION_MISMATCH,
                statement="digit reverse-plus-add lies outside residue-affine census language",
                evidence=LootEvidence.OBSERVED,
                experiment_id="reverse_and_add_base3",
                target="reverse_add_bt",
                failure_class=FailureClass.REPRESENTATION,
                bottleneck="outside_affine_valuation_control",
            ),
            GreyLoot(
                id="reverse_add_bt:loot:seed196",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement="seed 196 reaches 0 in eight steps; that is not a theorem on all integers",
                evidence=LootEvidence.PROVED,
                experiment_id="reverse_and_add_base3",
                target="reverse_add_bt",
            ),
            GreyLoot(
                id="reverse_add_bt:loot:cluster",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement="seed-196 finite closure is distinct from digit-fold saturation, aliquot truncation, and floor-power closure",
                evidence=LootEvidence.OBSERVED,
                experiment_id="reverse_and_add_base3",
                target="reverse_add_bt",
            ),
        ),
        "unresolved_questions": ("whether every integer seed hits a reverse-fixed point",),
    }
    experiment = experiment_from_session(
        session,
        spec,
        spec.attack_context(),
        experiment_id=LIVE_ID,
        target_family="nonlinear_integer",
        extra=extra,
        scout=ScoutDossier(
            target="reverse_and_add_base3",
            problem_definition=(
                "Does frozen v2.3 diagnose reverse-plus-add dynamics without a reverse-add attack or a totality theorem?"
            ),
            literature=("oeis-A134028",),
        ),
        prior_art=PriorArtMemory(
            literature_ids=("oeis-A134028",),
            independently_rediscovered=False,
            known_theorem_status="KNOWN",
        ),
    )
    store.add(experiment)
    store.finalize(LIVE_ID)
    payload = {
        "role": "flagship",
        "attack_table": _attack_table(session),
        "layer": "ENGINE REDISCOVERY",
        "baseline": tuple(item[0] for item in BASELINE),
        "failure_classes": tuple(item.failure_class.value for item in experiment.failures),
        "planner_unchanged_with_memory": unchanged,
        "strategy_chain": blind_strategy.plan.chain.id,
        "strategy_attacks": tuple(item.name for item in blind_strategy.results),
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
        strategy_chain=blind_strategy.plan.chain.id,
    )
    report.notes.append(
        f"{spec.name}: decision={summary.decision} chain={blind_strategy.plan.chain.id} "
        f"unchanged={unchanged} next={report.next_target_name}"
    )
    return memory_corpus, report
