"""Frozen ResearchLoop / StrategyPlanner campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.skolem_lrs.spec import CompanionShiftSpec
from research.skolem_order5_unconditional.discovery import evidence_state, falsify_claims
from research.skolem_order5_unconditional.planner import plan_map_session, plan_strategy
from research.skolem_order5_unconditional.scout import BASELINE
from research.skolem_order5_unconditional.spec import map_spec
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
from research_engine.strategy import ResearchGoal

CURRENT = "skolem_order5_unconditional"
LIVE_ID = "companion_shift_order5"


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
    summary.extra["vector_affine_status"] = table.get("vector_affine", "")
    summary.extra["matrix_word_status"] = table.get("matrix_word_invariant", "")
    results = {item.name: item for item in session.attack_report.results}
    census = results.get("vector_affine") or results.get("piecewise_affine")
    if census is not None:
        summary.extra["census_kind"] = census.evidence.get("census_kind")


def _yield_report(summary: SessionSummary, spec: CompanionShiftSpec) -> dict[str, Any]:
    evidence = evidence_state(spec)
    falsify = falsify_claims(spec)
    return {
        "known_rediscoveries": (
            f"engine decision {summary.decision}; skip {evidence['skipped_attacks']}"
        ),
        "new_exact_results": "first-coordinate zero at index 2; 25^5 skip matches 25^6",
        "new_invariants": "none; uniqueness is not recovered from moduli 2..32",
        "new_obstructions": "none; skip is COMPUTATION_EXHAUSTED, not a decision procedure",
        "new_origin_reachability_results": evidence["zero_at"],
        "new_nonreachability_results": "none; this instance has a ZERO_WITNESS",
        "new_quotients": "none",
        "new_control_constraints": "lattice/gcd uniqueness not obtained",
        "new_counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "new_conjectures": "none",
        "new_formalizations": "Problems.Engine.CompanionShift order-5 zero identity",
        "potentially_new_mathematics": "none claimed",
        "unresolved_questions": "unconditional vanishing for general order-5 LRS",
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
    blind_strategy = plan_strategy(spec, goal=ResearchGoal.ORIGIN_AVOIDANCE, memory=None)
    extra = {
        "computation_exhausted": True,
        "infinite_reachability_unresolved": False,
        "representation_novelty": NoveltyLevel.LOW.value,
        "mathematical_novelty": NoveltyLevel.NONE.value,
        "novelty_status": NoveltyStatus.KNOWN_REDISCOVERY.value,
        "engineering_changes": 0,
        "mathematical_yield": MathematicalYield(
            known_rediscoveries=(
                "order-5 companion window with a finite first-coordinate zero",
                "25^5 census and matrix-word skipped by the same frozen cell budget as d=6",
            ),
            new_exact_results=("first-coordinate zero at index 2",),
            new_formalizations=("Problems.Engine.CompanionShift",),
            new_obstructions=("none; uniqueness is not recovered; skip is not a decision",),
            new_counterexamples=("census skip at d=5 is the same cluster as d=6",),
            unresolved_questions=("unconditional vanishing for general order-5 LRS",),
            engineering_changes=0,
        ),
        "grey_loot": (
            GreyLoot(
                id="order5:loot:zero",
                kind=GreyLootKind.COUNTEREXAMPLE,
                statement="first coordinate vanishes at index 2 on the declared window",
                evidence=LootEvidence.PROVED,
                experiment_id="skolem_order5_unconditional",
                target="companion_shift_order5",
            ),
            GreyLoot(
                id="order5:loot:skip",
                kind=GreyLootKind.COMPUTATIONAL_BOTTLENECK,
                statement="25^5 census and matrix-word are skipped; same cluster as dimension 6",
                evidence=LootEvidence.FINITE_RANGE,
                experiment_id="skolem_order5_unconditional",
                target="companion_shift_order5",
            ),
            GreyLoot(
                id="order5:loot:uniqueness",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement="a ZERO_WITNESS is not uniqueness and not an unconditional order-5 procedure",
                evidence=LootEvidence.OBSERVED,
                experiment_id="skolem_order5_unconditional",
                target="companion_shift_order5",
            ),
        ),
        "unresolved_questions": ("unconditional vanishing for general order-5 LRS",),
    }
    experiment = experiment_from_session(
        session,
        spec,
        spec.attack_context(),
        experiment_id=LIVE_ID,
        target_family="linear_recurrence",
        extra=extra,
        scout=ScoutDossier(
            target="skolem_order5_unconditional",
            problem_definition=(
                "Can frozen v2.3 do more than exhaust a finite prefix on a declared order-5 window?"
            ),
            literature=(
                "lipton-et-al-2022-skolem-conjecture",
                "kenison-et-al-2025-order-4-skolem",
                "bacik-et-al-2026-skolem-positivity-survey",
            ),
        ),
        prior_art=PriorArtMemory(
            literature_ids=(
                "lipton-et-al-2022-skolem-conjecture",
                "kenison-et-al-2025-order-4-skolem",
                "bacik-et-al-2026-skolem-positivity-survey",
            ),
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
