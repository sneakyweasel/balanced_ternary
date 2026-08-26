"""Frozen ResearchLoop / StrategyPlanner campaign. No engine attacks are added."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from research.cyclic_tag_bit.discovery import evidence_state, falsify_claims
from research.cyclic_tag_bit.planner import plan_map_session, plan_strategy
from research.cyclic_tag_bit.scout import BASELINE
from research.cyclic_tag_bit.spec import WordRewriteSpec, map_spec
from research.engine_campaign.analysis import SessionSummary, summarize_session
from research.engine_campaign.corpus import seed_baseline_corpus
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

CURRENT = "cyclic_tag_bit"
LIVE_ID = "cyclic_tag"


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


def _yield_report(summary: SessionSummary, spec: WordRewriteSpec) -> dict[str, Any]:
    evidence = evidence_state(spec)
    falsify = falsify_claims(spec)
    return {
        "known_rediscoveries": (
            f"engine decision {summary.decision}; piecewise {summary.extra.get('piecewise_affine_status')}"
        ),
        "new_exact_results": "empty has no successor; [0] is fixed; 101 maps to 0111; length is nondecreasing",
        "new_invariants": "none promoted; length nondecrease is the rewrite definition",
        "new_obstructions": "none beyond the word rewrite; integer encoding is a mismatch",
        "new_origin_reachability_results": evidence["steps_to_empty"],
        "new_nonreachability_results": "nonempty window words do not map to empty in one step",
        "new_quotients": "none promoted",
        "new_control_constraints": "singleton dummy control only",
        "new_counterexamples": {
            key: item.get("counterexample")
            for key, item in falsify.items()
            if item.get("status") == "REFUTED"
        },
        "new_conjectures": "none",
        "new_formalizations": "Problems.Engine.CyclicTag",
        "potentially_new_mathematics": "none claimed",
        "unresolved_questions": "none on this production; nonempty length never drops",
        "engineering_changes": 0,
        "evidence": evidence,
        "falsify": falsify,
    }


def _representation_failure() -> FailureRecord:
    return FailureRecord(
        id="cyclic_tag:representation",
        target="cyclic_tag",
        experiment_id="cyclic_tag_bit",
        engine_version="0.2.1",
        phase="census",
        attack="piecewise_affine",
        failure_class=FailureClass.REPRESENTATION,
        representation_status="NON_AFFINE",
        mathematical_bottleneck="outside_affine_valuation_control",
        evidence="encoded word rewrite has no complete piecewise-affine cover on the sample window",
        reusable_lesson=(
            "Binary-word rewriting encoded as an integer is outside residue-affine language; "
            "the mismatch is the board prediction, not a tag-system attack and not a halt theorem "
            "from the frozen integer stack."
        ),
        prior_art_status="KNOWN",
        engineering_action="PARK",
        research_value=ImportanceLevel.MEDIUM,
        status=FailureStatus.PARKED,
        affected_attack_family="latent_affine",
        minimal_example="0w |-> w0 ; 1w |-> w11",
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
        "computation_exhausted": True,
        "infinite_reachability_unresolved": False,
        "representation_novelty": NoveltyLevel.HIGH.value,
        "mathematical_novelty": NoveltyLevel.NONE.value,
        "novelty_status": NoveltyStatus.KNOWN_REDISCOVERY.value,
        "engineering_changes": 0,
        "failures": (_representation_failure(),),
        "mathematical_yield": MathematicalYield(
            known_rediscoveries=(
                "empty has no successor; length is nondecreasing",
                "no complete piecewise-affine cover",
            ),
            new_exact_results=("tagStep [] = none", "101 maps to 0111", "[0] is fixed"),
            new_formalizations=("Problems.Engine.CyclicTag",),
            new_obstructions=("none; integer encoding is the predicted mismatch",),
            new_counterexamples=("nonempty window words do not drop length",),
            unresolved_questions=("none on this production",),
            engineering_changes=0,
        ),
        "grey_loot": (
            GreyLoot(
                id="cyclic_tag:loot:mismatch",
                kind=GreyLootKind.REPRESENTATION_MISMATCH,
                statement="binary-word rewriting encoded as an integer lies outside residue-affine census language",
                evidence=LootEvidence.OBSERVED,
                experiment_id="cyclic_tag_bit",
                target="cyclic_tag",
                failure_class=FailureClass.REPRESENTATION,
                bottleneck="outside_affine_valuation_control",
            ),
            GreyLoot(
                id="cyclic_tag:loot:seed101",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement="seed 101 maps to 0111 and grows; empty is not reached; that is the rewrite, not an integer halt theorem",
                evidence=LootEvidence.PROVED,
                experiment_id="cyclic_tag_bit",
                target="cyclic_tag",
            ),
            GreyLoot(
                id="cyclic_tag:loot:cluster",
                kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                statement="EXPANDING / UNBOUNDED_SAMPLE on the encoding is the predicted word/integer mismatch, not a reusable affine lesson",
                evidence=LootEvidence.OBSERVED,
                experiment_id="cyclic_tag_bit",
                target="cyclic_tag",
            ),
        ),
        "unresolved_questions": ("none on this production",),
    }
    experiment = experiment_from_session(
        session,
        spec,
        spec.attack_context(),
        experiment_id=LIVE_ID,
        target_family="word_rewrite",
        extra=extra,
        scout=ScoutDossier(
            target="cyclic_tag_bit",
            problem_definition=(
                "Does frozen v2.3 diagnose encoded word rewriting without a tag-system attack?"
            ),
            literature=("baader-nipkow-1998-term-rewriting",),
        ),
        prior_art=PriorArtMemory(
            literature_ids=("baader-nipkow-1998-term-rewriting",),
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
