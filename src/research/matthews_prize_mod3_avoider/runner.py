"""Frozen ResearchLoop / StrategyPlanner campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.linear_constraint_loops.spec import OneVariableLoopSpec
from research.matthews_prize_mod3_avoider.discovery import evidence_state, falsify_claims
from research.matthews_prize_mod3_avoider.planner import plan_map_session, plan_strategy
from research.matthews_prize_mod3_avoider.scout import BASELINE
from research.matthews_prize_mod3_avoider.spec import map_spec
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

CURRENT = "matthews_prize_mod3_avoider"


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
        "new_exact_results": "0 (mod 3) invariant and expanding; cycles at -1 and {-2,-4}",
        "new_invariants": "3|x implies 3|T(x)",
        "new_obstructions": "none; avoider-class forcing into cycles is not obtained",
        "new_origin_reachability_results": evidence["seed1_hits_zero_mod_three"],
        "new_nonreachability_results": "seeds 1 and 5 are not avoiders; they enter 0 (mod 3)",
        "new_quotients": "{1,2} (mod 3) is not a basin",
        "new_control_constraints": "three residue-affine branches; generic cycle words",
        "new_counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "new_conjectures": "none",
        "new_formalizations": "Problems.Engine.MatthewsMod3",
        "potentially_new_mathematics": "none claimed",
        "unresolved_questions": "whether every Z-avoider enters -1 or {-2,-4}",
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
                "three residue-affine branches 2x / (7x+2)/3 / (x-2)/3",
                "generic control-word cycle obstructions",
            ),
            new_exact_results=(
                "0 (mod 3) is invariant and expanding",
                "cycles at -1 and {-2,-4}",
            ),
            new_formalizations=("Problems.Engine.MatthewsMod3",),
            new_obstructions=("none; avoider-class forcing into cycles is not obtained",),
            new_counterexamples=(
                "seeds 1 and 5 enter 0 (mod 3)",
                "{1,2} (mod 3) is not a basin",
                "window avoiders include preimages -28 and -10, not only cycle points",
            ),
            unresolved_questions=("whether every Z-avoider enters -1 or {-2,-4}",),
            engineering_changes=0,
        ),
        "grey_loot": (
            GreyLoot(
                id="matthews_mod3:loot:zero",
                kind=GreyLootKind.CANDIDATE_INVARIANT,
                statement="if 3|x then T(x)=2x and 3|T(x)",
                evidence=LootEvidence.PROVED,
                experiment_id="matthews_prize_mod3_avoider",
                target="mod3_three_branch",
            ),
            GreyLoot(
                id="matthews_mod3:loot:seeds",
                kind=GreyLootKind.COUNTEREXAMPLE,
                statement="packet seeds 1 and 5 enter 0 (mod 3); {1,2} (mod 3) is not a basin",
                evidence=LootEvidence.PROVED,
                experiment_id="matthews_prize_mod3_avoider",
                target="mod3_three_branch",
            ),
            GreyLoot(
                id="matthews_mod3:loot:branches",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement="three-branch census is the problem definition, not an avoider-class obstruction",
                evidence=LootEvidence.KNOWN,
                experiment_id="matthews_prize_mod3_avoider",
                target="mod3_three_branch",
            ),
        ),
        "unresolved_questions": ("whether every Z-avoider enters -1 or {-2,-4}",),
    }
    experiment = experiment_from_session(
        session,
        spec,
        spec.attack_context(),
        experiment_id="mod3_three_branch",
        target_family="residue_affine",
        extra=extra,
        scout=ScoutDossier(
            target="matthews_prize_mod3_avoider",
            problem_definition=(
                "On the three-branch mod-3 map, does a class obstruction force avoiders into the known cycles?"
            ),
            literature=("matthews-watts-1984-generalization-hasse",),
        ),
        prior_art=PriorArtMemory(
            literature_ids=("matthews-watts-1984-generalization-hasse",),
            independently_rediscovered=False,
            known_theorem_status="KNOWN",
        ),
    )
    store.add(experiment)
    store.finalize("mod3_three_branch")
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
