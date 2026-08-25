"""Research Engine v2.2 memory: classification, loot, clustering, hygiene, selection."""

from __future__ import annotations

from dataclasses import dataclass, replace

from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import ResearchLoop
from research_engine.diagnosis.selection import score_candidate
from research_engine.diagnosis.types import CandidateSketch, RegimeFingerprint
from research_engine.memory.classify import FailureSignals, classify_signals
from research_engine.memory.hygiene import leak_hits
from research_engine.memory.retrieval import assert_not_injected
from research_engine.memory.seed_records import historical_experiments
from research_engine.memory.store import FinalizedError, ResearchMemory
from research_engine.memory.types import (
    DecisionReason,
    EngineeringRecommendation,
    FailureClass,
    GreyLootKind,
    LootEvidence,
    MemoryLane,
    NoveltyLevel,
    NoveltyStatus,
    Reconciliation,
)
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER


@dataclass(frozen=True)
class FoldSpec:
    name: str = "memory_fold"
    dimension: int = 1
    start: int = 8
    start_remaining: int = 6

    @property
    def initial_state(self) -> tuple[int, ...]:
        return (self.start,)

    def transition(self, state: tuple[int, ...], control: object, phase: IntPhase) -> tuple[int, ...]:
        del control, phase
        n = state[0]
        if n == 0:
            return (0,)
        return (n // 2 if abs(n) > 1 else 0,)

    def output(self, state: tuple[int, ...], control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return int(state[0])

    def legal_controls(self, state: tuple[int, ...], phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (0,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        del state
        return phase.value >= 0

    def is_accepting(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        del state
        return phase.value == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: tuple[int, ...]) -> tuple[int, ...]:
        return (int(state[0]),)

    def attack_context(self) -> AttackContext:
        return AttackContext(live_only=False, max_states=32, max_steps=self.start_remaining)


def _memory() -> ResearchMemory:
    return ResearchMemory(historical_experiments())


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert DEFAULT_ATTACK_ORDER.index("matrix_word_invariant") == DEFAULT_ATTACK_ORDER.index("vector_affine") + 1


def test_known_failures_classify_to_expected_classes():
    memory = _memory()
    by_id = {item.experiment_id: item for item in memory.experiments}
    assert any(f.failure_class is FailureClass.REPRESENTATION for f in by_id["aliquot_276"].failures)
    assert any(f.failure_class is FailureClass.QUANTIFIER for f in by_id["sum_strip_slc"].failures)
    globals_skolem = [f for f in by_id["skolem_order6"].failures if f.failure_class is FailureClass.GLOBAL_REASONING]
    compute = [f for f in by_id["skolem_order6"].failures if f.failure_class is FailureClass.COMPUTATIONAL]
    assert globals_skolem and compute
    globals_pos = [f for f in by_id["positivity_order10"].failures if f.failure_class is FailureClass.GLOBAL_REASONING]
    assert globals_pos
    switching = by_id["switching_affine_z2_origin"]
    assert switching.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
    assert all(f.failure_class is not FailureClass.GLOBAL_REASONING for f in switching.failures)
    hygiene = by_id["skolem_lrs_hygiene"].failures[0]
    assert hygiene.failure_class is FailureClass.EXPERIMENT_HYGIENE
    assert hygiene.status.value == "RESOLVED"
    involution = by_id["involution_census"].failures[0]
    assert involution.failure_class is FailureClass.DOMAIN_INFERENCE
    assert involution.engineering_action == "DO_NOT_IMPLEMENT"


def test_live_classifier_matches_seed_signals():
    aliquot = classify_signals(
        FailureSignals(
            target="aliquot_276",
            experiment_id="aliquot_276",
            decision="ENGINE_LIMITATION",
            census_kind="UNRESOLVED",
            transition_unresolved=True,
        )
    )
    assert aliquot[0].failure_class is FailureClass.REPRESENTATION
    quant = classify_signals(
        FailureSignals(
            target="sum_strip",
            experiment_id="sum_strip_slc",
            decision="ENGINE_LIMITATION",
            overlapping_branches=True,
        )
    )
    assert any(item.failure_class is FailureClass.QUANTIFIER for item in quant)


def test_global_and_quantifier_clusters_are_not_by_target_name():
    memory = _memory()
    clusters = {item.id: item for item in memory.clusters()}
    global_keys = [key for key in clusters if key.startswith("GLOBAL_REASONING")]
    quant_keys = [key for key in clusters if key.startswith("QUANTIFIER")]
    assert global_keys
    assert quant_keys
    global_cluster = clusters[global_keys[0]]
    assert global_cluster.recurrence_count >= 3
    assert global_cluster.target_diversity >= 3
    assert "companion_shift_order6" in global_cluster.targets
    assert "companion_obs_order10" in global_cluster.targets
    assert "rplus" in global_cluster.targets
    assert "bb5_map" in global_cluster.targets
    assert "two_path_z2" not in global_cluster.targets
    assert "sum_strip" not in global_cluster.targets
    quant_cluster = clusters[quant_keys[0]]
    assert quant_cluster.recurrence_count >= 2
    assert "sum_strip" in quant_cluster.targets
    assert "companion_shift_order6" not in quant_cluster.targets
    assert all("|" in item.id for item in memory.clusters())


def test_grey_loot_survives_finalize_and_json_roundtrip():
    memory = _memory()
    skolem = memory.get("skolem_order6")
    assert skolem.finalized
    assert skolem.grey_loot
    kinds = {item.kind for item in skolem.grey_loot}
    assert GreyLootKind.COUNTEREXAMPLE in kinds
    loaded = ResearchMemory.load_historical()
    again = loaded.get("skolem_order6")
    assert again.grey_loot == skolem.grey_loot
    loot = loaded.query_loot(kind=GreyLootKind.COUNTEREXAMPLE, target="companion_shift_order6")
    assert loot
    try:
        loaded.add(replace(skolem, grey_loot=()))
        raise AssertionError("finalized experiment was overwritten")
    except FinalizedError:
        pass
    loaded.reconcile("skolem_order6", Reconciliation(notes="prior-art overlay"))
    assert loaded.get("skolem_order6").reconciliation is not None
    assert loaded.get("skolem_order6").grey_loot


def test_known_rediscovery_is_not_marked_novel():
    memory = _memory()
    for exp_id in ("syracuse", "carelli_rplus", "bb5_map"):
        item = memory.get(exp_id)
        assert item.representation_novelty is NoveltyLevel.HIGH
        assert item.mathematical_novelty is NoveltyLevel.NONE
        assert item.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
        assert item.prior_art is not None
        assert item.prior_art.semantic_equivalents
        assert item.prior_art.semantic_equivalents[0].known_equivalent is True
        assert item.prior_art.semantic_equivalents[0].mathematical_meaning == "equivalent"


def test_lanes_keep_scout_out_of_blind_packets():
    memory = _memory()
    scout = memory.scout_for("companion_shift_order6")
    assert scout is not None
    assert "Skolem" in scout.problem_definition or scout.literature
    packet = memory.blind_packet_for("skolem_order6")
    assert packet.spec_name == "companion_shift_order6"
    assert "scout" not in packet.as_dict()
    assert "literature" not in packet.extra
    blob = repr(packet.as_dict())
    assert "Bacik" not in blob
    assert "p-adic" not in blob
    loot = memory.grey_loot()
    assert_not_injected(packet, loot)
    attack_lane = memory.lane(MemoryLane.ATTACK)
    scout_lane = memory.lane(MemoryLane.SCOUT)
    assert packet in attack_lane
    assert scout in scout_lane
    ctx = AttackContext()
    memory.query_loot(evidence=LootEvidence.REFUTED)
    assert ctx.skip_attacks == ()


def test_score_without_memory_matches_legacy_formula():
    corpus = ResearchCorpus()
    sketch = CandidateSketch(name="toy", experimental_cost=2.0, claimed_capabilities=("finite_closure",))
    report = score_candidate(sketch, corpus)
    expected = (1.0 * 1.0 * 1.0 * 1.0) / 2.0
    assert report.value == expected
    assert report.failure_learning_value == 1.0
    assert "failure_learning" not in report.explanation
    again = score_candidate(sketch, corpus, memory=None)
    assert again.value == report.value
    assert again.explanation == report.explanation


def test_failure_history_changes_expected_research_value():
    memory = _memory()
    corpus = ResearchCorpus(tuple(item.diagnosis for item in memory.experiments))
    saturated = CandidateSketch(
        name="another_scalar_fold",
        fingerprint=RegimeFingerprint(
            state_space_type="INTEGER_1D",
            control_structure="SINGLETON",
            numerical_contraction="FINITE_CONTRACTING",
            eventual_region="FINITE_SEED_CLOSURE",
        ),
        claimed_capabilities=("finite_closure", "numerical_contraction"),
        experimental_cost=1.0,
    )
    distant = CandidateSketch(
        name="open_global_reachability",
        fingerprint=RegimeFingerprint(
            state_space_type="INTEGER_VECTOR",
            control_structure="SINGLETON",
            numerical_contraction="MIXED_MAGNITUDE",
            eventual_region="UNBOUNDED_SAMPLE",
            affine_control_type="VECTOR",
        ),
        claimed_capabilities=("infinite_reachable_trajectories", "latent_vector_affine_control"),
        experimental_cost=1.0,
    )
    without_sat = score_candidate(saturated, corpus)
    without_dist = score_candidate(distant, corpus)
    with_sat = score_candidate(saturated, corpus, memory=memory)
    with_dist = score_candidate(distant, corpus, memory=memory)
    assert with_sat.failure_learning_value < 1.0
    assert with_dist.failure_learning_value > 1.0
    assert "GLOBAL_REASONING" in with_dist.explanation
    assert with_dist.value > with_sat.value
    assert without_sat.failure_learning_value == 1.0
    assert without_dist.failure_learning_value == 1.0


def test_historical_regression_classes_are_stable():
    live = {item.experiment_id: item for item in historical_experiments()}
    frozen = {item.experiment_id: item for item in ResearchMemory.load_historical().experiments}
    assert set(live) == set(frozen)
    for exp_id, item in live.items():
        other = frozen[exp_id]
        assert tuple(f.failure_class for f in other.failures) == tuple(f.failure_class for f in item.failures)
        assert other.novelty_status is item.novelty_status
        assert other.diagnosis.fingerprint.as_dict() == item.diagnosis.fingerprint.as_dict()


def test_hygiene_allowlists_problem_ids_but_not_bare_literature_tokens():
    allowed = leak_hits("from research.skolem_lrs.spec import map_spec\n", ("skolem", "Skolem"))
    assert allowed == ()
    leaked = leak_hits("The Skolem Problem is encoded here.\n", ("skolem", "Skolem"))
    assert "Skolem" in leaked
    assert leak_hits("companion_shift_order6", ("skolem", "Skolem")) == ()


def test_engineering_policy_does_not_auto_implement():
    memory = _memory()
    recs = {item.failure_cluster: item.recommendation for item in memory.engineering_candidates()}
    global_ids = [key for key in recs if key.startswith("GLOBAL_REASONING")]
    assert global_ids
    assert recs[global_ids[0]] is EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION
    quant_ids = [key for key in recs if key.startswith("QUANTIFIER")]
    assert quant_ids
    assert recs[quant_ids[0]] is not EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION
    backlog = memory.engineering_backlog()
    assert all(item.reason_not_implemented_yet for item in backlog)
    questions = [q for cluster in memory.clusters() for q in cluster.research_questions]
    assert any("finite reachability" in q.statement for q in questions)


def test_research_loop_outputs_stable_with_and_without_memory():
    spec = FoldSpec()
    ctx = spec.attack_context()
    plain = ResearchLoop().run(spec, ctx)
    store = ResearchMemory()
    wrapped = ResearchLoop().run(spec, ctx, memory=store)
    assert tuple((item.name, item.status, item.claim) for item in plain.attack_report.results) == tuple(
        (item.name, item.status, item.claim) for item in wrapped.attack_report.results
    )
    assert plain.decision is wrapped.decision
    assert plain.decision_reason == wrapped.decision_reason
    assert store.experiments
    assert store.experiments[0].finalized
    assert store.experiments[0].blind_packet is not None
    assert store.experiments[0].blind_packet.spec_name == spec.name


def test_yield_and_decision_reason_are_recorded():
    item = _memory().get("aliquot_276")
    assert item.decision_reason_code is DecisionReason.REPRESENTATION_MISMATCH
    assert item.mathematical_yield.engineering_changes == 0
    assert item.mathematical_yield.unresolved_questions
    assert item.diagnosis.lean_certificate
    syr = _memory().get("syracuse")
    assert syr.decision_reason_code is DecisionReason.KNOWN_REDISCOVERY
    assert "latent residue control" in syr.mathematical_yield.new_terminology
