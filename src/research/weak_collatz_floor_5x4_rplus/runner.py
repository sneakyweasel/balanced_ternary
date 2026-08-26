"""Frozen ResearchLoop / StrategyPlanner campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.linear_constraint_loops.spec import OneVariableLoopSpec
from research.weak_collatz_floor_5x4_rplus.discovery import evidence_state, falsify_claims
from research.weak_collatz_floor_5x4_rplus.planner import plan_map_session, plan_strategy
from research.weak_collatz_floor_5x4_rplus.scout import BASELINE
from research.weak_collatz_floor_5x4_rplus.spec import map_spec
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

CURRENT = "weak_collatz_floor_5x4_rplus"


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
    census = results.get("piecewise_affine")
    if census is not None:
        summary.extra["census_kind"] = census.evidence.get("census_kind")
        family = census.evidence.get("family")
        if isinstance(family, dict):
            summary.extra["family"] = dict(family)
        branches = census.evidence.get("branches")
        if branches:
            summary.extra["branches"] = tuple(dict(item) for item in branches)
            summary.extra["branch_count"] = len(tuple(branches))
    obstructed = results.get("control_obstruction")
    if obstructed is not None:
        summary.extra["obstruction_claim"] = obstructed.claim
        summary.extra["obstruction_status"] = obstructed.status.value
        summary.extra["class_count"] = obstructed.evidence.get("class_count")
        summary.extra["symbolic_count"] = obstructed.evidence.get("symbolic_count")
        summary.extra["recursive_count"] = obstructed.evidence.get("recursive_count")


def _yield_report(summary: SessionSummary, spec: OneVariableLoopSpec) -> dict[str, Any]:
    evidence = evidence_state(spec)
    falsify = falsify_claims(spec)
    return {
        "known_rediscoveries": (
            f"engine decision {summary.decision}; census {summary.census_kind or 'none'}"
        ),
        "new_exact_results": "unique successor on x>=2; successor stays in the domain",
        "new_invariants": "4y = 5x-r for r in {1,2,3,4} on residues mod 4",
        "new_obstructions": "none; losing the successor is false on this closed strip",
        "new_origin_reachability_results": evidence["path_undefined"],
        "new_nonreachability_results": "seed 5 grows on horizons 16 and 32; not a halt theorem",
        "new_quotients": "x>=2 -> unique successor; not a basin exclusion",
        "new_control_constraints": "four residue-affine branches; generic cycle words",
        "new_counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "new_conjectures": "none",
        "new_formalizations": "Problems.Engine.LinearConstraintLoops floor54Rel lemmas",
        "potentially_new_mathematics": "none claimed",
        "unresolved_questions": "weak-map halt is a different spec, not this closed strip",
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
    blind_strategy = plan_strategy(spec, goal=ResearchGoal.CYCLE_EXCLUSION, memory=None)
    extra = {
        "computation_exhausted": False,
        "infinite_reachability_unresolved": False,
        "representation_novelty": NoveltyLevel.MEDIUM.value,
        "mathematical_novelty": NoveltyLevel.NONE.value,
        "novelty_status": NoveltyStatus.KNOWN_REDISCOVERY.value,
        "engineering_changes": 0,
        "mathematical_yield": MathematicalYield(
            known_rediscoveries=(
                "four residue-affine branches 4y=5x-r",
                "generic control-word cycle obstructions",
            ),
            new_exact_results=(
                "unique successor for every x>=2",
                "a defined successor stays in x>=2",
            ),
            new_formalizations=("Problems.Engine.LinearConstraintLoops",),
            new_obstructions=("none; losing the successor is false on this closed strip",),
            new_counterexamples=(
                "fixed points 2,3,4 never lose a successor",
                "seed 5 grows on horizons 16 and 32",
                "T_strip(8)=9 while R+(8)=10",
            ),
            unresolved_questions=("weak-map halt is a different spec",),
            engineering_changes=0,
        ),
        "grey_loot": (
            GreyLoot(
                id="floor_5x4:loot:unique",
                kind=GreyLootKind.CANDIDATE_INVARIANT,
                statement="every x>=2 has a unique integer successor on 5x-4 <= 4x' <= 5x-1",
                evidence=LootEvidence.PROVED,
                experiment_id="weak_collatz_floor_5x4_rplus",
                target="floor_5x4_strip",
            ),
            GreyLoot(
                id="floor_5x4:loot:never_drops",
                kind=GreyLootKind.COUNTEREXAMPLE,
                statement="fixed points 2,3,4 and the growing orbit of 5 never lose a successor",
                evidence=LootEvidence.PROVED,
                experiment_id="weak_collatz_floor_5x4_rplus",
                target="floor_5x4_strip",
            ),
            GreyLoot(
                id="floor_5x4:loot:reparam",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement="four residue-affine branches are a 4/3 SLC reparameterization, not a halt obstruction",
                evidence=LootEvidence.KNOWN,
                experiment_id="weak_collatz_floor_5x4_rplus",
                target="floor_5x4_strip",
            ),
        ),
        "unresolved_questions": ("weak-map halt is a different spec",),
    }
    experiment = experiment_from_session(
        session,
        spec,
        spec.attack_context(),
        experiment_id="floor_5x4_strip",
        target_family="linear_constraint_loop",
        extra=extra,
        scout=ScoutDossier(
            target="weak_collatz_floor_5x4_rplus",
            problem_definition=(
                "On 5x-4 <= 4x' <= 5x-1 with x>=2, does a class obstruction constrain losing the successor?"
            ),
            literature=(
                "carelli-2026-loop-termination",
                "matthews-watts-1984-generalization-hasse",
                "ben-amram-genaim-ouaknine-worrell-2025-termination-survey",
            ),
        ),
        prior_art=PriorArtMemory(
            literature_ids=(
                "carelli-2026-loop-termination",
                "matthews-watts-1984-generalization-hasse",
                "ben-amram-genaim-ouaknine-worrell-2025-termination-survey",
            ),
            independently_rediscovered=False,
            known_theorem_status="KNOWN",
        ),
    )
    store.add(experiment)
    store.finalize("floor_5x4_strip")
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
    summary.extra["latent_control_obstruction"] = fp.latent_control_obstruction
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
        f"{spec.name}: decision={summary.decision} census={summary.census_kind or 'none'} "
        f"chain={blind_strategy.plan.chain.id} unchanged={unchanged} next={report.next_target_name}"
    )
    return memory_corpus, report
