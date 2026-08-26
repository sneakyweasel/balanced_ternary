"""Frozen ResearchLoop / StrategyPlanner campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
from research.mx_plus_r_7x1_class_obstruction.discovery import evidence_state, falsify_claims
from research.mx_plus_r_7x1_class_obstruction.planner import plan_map_session, plan_strategy
from research.mx_plus_r_7x1_class_obstruction.scout import BASELINE
from research.mx_plus_r_7x1_class_obstruction.spec import map_spec
from research.mx_plus_r.spec import MxPlusRSpec
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

CURRENT = "mx_plus_r_7x1_class_obstruction"


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
    obstructed = results.get("control_obstruction")
    if obstructed is not None:
        summary.extra["obstruction_claim"] = obstructed.claim
        summary.extra["obstruction_status"] = obstructed.status.value
        summary.extra["class_count"] = obstructed.evidence.get("class_count")
        summary.extra["symbolic_count"] = obstructed.evidence.get("symbolic_count")
        summary.extra["recursive_count"] = obstructed.evidence.get("recursive_count")


def _yield_report(summary: SessionSummary, spec: MxPlusRSpec) -> dict[str, Any]:
    evidence = evidence_state(spec)
    falsify = falsify_claims(spec)
    return {
        "known_rediscoveries": (
            f"engine decision {summary.decision}; census {summary.census_kind or 'none'}"
        ),
        "new_exact_results": "T(n) ≡ 1,2,4 (mod 7); only positive 1-cycle is 1",
        "new_invariants": "image of T lies in the subgroup <2> of (Z/7Z)*",
        "new_obstructions": "image class, not a basin exclusion from C_out",
        "new_origin_reachability_results": evidence["hits_one_horizon_16"],
        "new_nonreachability_results": "seed 3 misses 1 on horizons 16 and 32; not divergence",
        "new_quotients": "odd integers -> image class {1,2,4} (mod 7) after one step",
        "new_control_constraints": "singleton dummy control; recovered 2^k y = 7x+1",
        "new_counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "new_conjectures": "none",
        "new_formalizations": "Problems.Engine.MxPlusR image-class lemmas",
        "potentially_new_mathematics": "none claimed",
        "unresolved_questions": "which odd n reach 1; not answered by the image class",
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
                "parameterized family 2^k y = 7x+1",
                "generic control-word cycle obstructions",
            ),
            new_exact_results=(
                "image of T lies in {n odd : n ≡ 1,2,4 (mod 7)}",
                "only positive length-one cycle is 1",
            ),
            new_formalizations=("Problems.Engine.MxPlusR",),
            new_obstructions=("image class <2> in (Z/7Z)*; not a basin exclusion",),
            new_counterexamples=(
                "73 ≡ 3 (mod 7) maps to 1",
                "299593 ≡ 0 (mod 7) maps to 1",
            ),
            unresolved_questions=("which odd n reach 1",),
            engineering_changes=0,
        ),
        "grey_loot": (
            GreyLoot(
                id="mx_plus_r_7x1:loot:image",
                kind=GreyLootKind.CANDIDATE_INVARIANT,
                statement="T(n) ≡ 1, 2, or 4 (mod 7) for every odd positive n",
                evidence=LootEvidence.PROVED,
                experiment_id="mx_plus_r_7x1_class_obstruction",
                target="mx_plus_r_7_1",
            ),
            GreyLoot(
                id="mx_plus_r_7x1:loot:out_class",
                kind=GreyLootKind.COUNTEREXAMPLE,
                statement="73 ≡ 3 (mod 7) and 299593 ≡ 0 (mod 7) both map to 1",
                evidence=LootEvidence.PROVED,
                experiment_id="mx_plus_r_7x1_class_obstruction",
                target="mx_plus_r_7_1",
            ),
            GreyLoot(
                id="mx_plus_r_7x1:loot:family",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement="family rediscovery and generic cycle words are not a basin obstruction to 1",
                evidence=LootEvidence.KNOWN,
                experiment_id="mx_plus_r_7x1_class_obstruction",
                target="mx_plus_r_7_1",
            ),
        ),
        "unresolved_questions": ("which odd n reach 1",),
    }
    experiment = experiment_from_session(
        session,
        spec,
        spec.attack_context(),
        experiment_id="mx_plus_r_7_1",
        target_family="mx_plus_r",
        extra=extra,
        scout=ScoutDossier(
            target="mx_plus_r_7x1_class_obstruction",
            problem_definition=(
                "On T(x)=(7x+1)/2^{v_2(7x+1)}, does a class obstruction constrain reaching 1?"
            ),
            literature=("crandall-1978-3x+1", "chamberland-2003-3x+1-survey"),
        ),
        prior_art=PriorArtMemory(
            literature_ids=("crandall-1978-3x+1", "chamberland-2003-3x+1-survey"),
            independently_rediscovered=False,
            known_theorem_status="KNOWN",
        ),
    )
    store.add(experiment)
    store.finalize("mx_plus_r_7_1")
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
