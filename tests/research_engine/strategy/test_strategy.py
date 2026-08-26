"""v2.3 Phase 1: hypotheses, opt-in strategy, blindness, frozen flood planner."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.hidden_piecewise import HiddenPowerClearDSpec, HiddenSignBSpec
from research_engine.diagnosis.loop import ResearchLoop
from research_engine.memory.retrieval import assert_hypotheses_not_injected
from research_engine.memory.store import ResearchMemory
from research_engine.memory.types import BlindPacket, NoveltyStatus
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, DEFAULT_ATTACK_ORDER
from research_engine.strategy import (
    CENSUS_OBSTRUCTION_CHAIN,
    ENGINE_STRATEGY_VERSION,
    GLOBAL_INDUCTIVE_CHAIN,
    ResearchGoal,
    ResearchHypothesis,
    ResearchHypothesisStatus,
    StrategyPlanner,
    falsify,
    freeze_attack_order,
    generate_from_memory,
    remember_hypotheses,
    select_chain,
)
from research_engine.strategy.types import ObligationKind, ProofObligation
from tests.research_engine.core.test_planner import CountdownSpec


def _memory() -> ResearchMemory:
    return ResearchMemory.load_historical()


def _by_target(hyps, target: str) -> list[ResearchHypothesis]:
    return [item for item in hyps if item.target == target]


def test_strategy_version_and_frozen_order():
    assert ENGINE_STRATEGY_VERSION == "0.2.3"
    assert freeze_attack_order() == DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert CENSUS_OBSTRUCTION_CHAIN.attacks == (
        "piecewise_affine",
        "parameter_domain",
        "control_word",
        "control_obstruction",
    )
    assert GLOBAL_INDUCTIVE_CHAIN.id not in DEFAULT_ATTACK_ORDER
    assert "global_inductive" not in DEFAULT_ATTACK_ORDER


def test_historical_memory_loads_without_hypotheses_key():
    memory = _memory()
    assert memory.hypotheses() == ()
    dumped = memory.as_dict()
    assert dumped["hypotheses"] == []
    restored = ResearchMemory.from_dict({"experiments": dumped["experiments"]})
    assert restored.hypotheses() == ()
    assert len(restored.experiments) == len(memory.experiments)


def test_replay_syracuse_carelli_switching_matrix_are_known():
    hyps = generate_from_memory(_memory())
    assert hyps

    syracuse = _by_target(hyps, "syracuse")
    assert any("2^k y = 3x+1" in item.statement or "3x+1" in item.statement for item in syracuse)
    assert any("class" in item.statement.lower() and "obstruction" in item.statement.lower() or "elimination" in item.statement.lower() for item in syracuse)
    assert all(item.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY for item in syracuse)
    assert all(item.prior_art_matches for item in syracuse)
    assert all(item.source_target == "syracuse" for item in syracuse)

    rplus = _by_target(hyps, "rplus")
    assert any("3y=4x-1" in item.statement or "4x-1" in item.statement for item in rplus)
    assert all(item.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY for item in rplus)
    assert any(item.cluster_id == "global_reachability" for item in rplus)

    switching = _by_target(hyps, "two_path_z2")
    assert any("N^2" in item.statement or "nonnegative" in item.statement.lower() for item in switching)
    assert all(item.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY for item in switching)

    matrix = _by_target(hyps, "matrix_word_invariant")
    assert any("lattice" in item.statement.lower() or "gcd" in item.statement.lower() for item in matrix)
    assert all(item.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY for item in matrix)


def test_known_identity_is_search_supported_without_ledger_promote():
    hyps = generate_from_memory(_memory())
    syracuse = [item for item in hyps if item.target == "syracuse"]
    supported = [
        item
        for item in syracuse
        if item.current_status
        in {
            ResearchHypothesisStatus.SEARCH_SUPPORTED,
            ResearchHypothesisStatus.PROVED,
            ResearchHypothesisStatus.LEAN_CERTIFIED,
            ResearchHypothesisStatus.PROOF_READY,
        }
    ]
    assert supported
    ledger = ResearchLedger()
    for item in supported:
        ledger.add_hypothesis(
            Hypothesis(
                id=item.id,
                statement=item.statement,
                kind=item.kind,
                intended_scope=item.intended_scope,
                status=HypothesisStatus.OPEN,
            )
        )
        assert ledger.get(item.id).status is HypothesisStatus.OPEN
    assert ledger.decisions == []


def test_planted_false_invariant_is_refuted():
    spec = HiddenSignBSpec()
    hyp = ResearchHypothesis(
        id="hyp:planted:nonneg_singleton",
        statement="S={(0,)} is an invariant region",
        target=spec.name,
        source_target=spec.name,
        current_status=ResearchHypothesisStatus.CANDIDATE,
        proof_obligations=(
            ProofObligation(kind=ObligationKind.INDUCTIVE_INCLUSION, statement="Need: T(S) ⊆ S"),
        ),
    )
    result = falsify(
        hyp,
        spec,
        AttackContext(candidate_region=frozenset({(0,)}), live_only=False, max_steps=8),
    )
    assert result.current_status is ResearchHypothesisStatus.REFUTED
    assert result.counterexamples


def test_planner_rediscovers_census_obstruction_chain():
    spec = HiddenPowerClearDSpec()
    context = spec.attack_context()
    flood = AttackPlanner().run(spec, context)
    plan = select_chain(spec, ResearchGoal.CYCLE_EXCLUSION)
    assert plan.chain.id == "census_obstruction"
    assert plan.chain.attacks == CENSUS_OBSTRUCTION_CHAIN.attacks

    report = StrategyPlanner().run(spec, context, goal=ResearchGoal.CYCLE_EXCLUSION)
    names = [item.name for item in report.results]
    assert names[:4] == list(CENSUS_OBSTRUCTION_CHAIN.attacks) or set(CENSUS_OBSTRUCTION_CHAIN.attacks) <= set(names)
    assert len(report.results) < len(flood.results)
    obstruction = next(item for item in report.results if item.name == "control_obstruction")
    assert obstruction.status is AttackStatus.SUPPORTED
    assert report.metrics.attacks_executed < len(DEFAULT_ATTACK_ORDER)
    assert report.metrics.useful_results >= 1
    assert report.attempted_chains[0] == "census_obstruction"


def test_default_planner_and_research_loop_still_flood():
    spec = HiddenPowerClearDSpec()
    context = spec.attack_context()
    flood = AttackPlanner().run(spec, context)
    loop = ResearchLoop().run(spec, context, record=False)
    assert [item.name for item in flood.results] == [item.name for item in loop.attack_report.results]
    assert "reconnaissance" in [item.name for item in flood.results]
    strategy = StrategyPlanner().run(spec, context, goal=ResearchGoal.CYCLE_EXCLUSION)
    assert "reconnaissance" not in [item.name for item in strategy.results]


def test_countdown_default_planner_unchanged_shape():
    spec = CountdownSpec()
    report = AttackPlanner().run(spec, AttackContext(live_only=True, max_steps=4))
    names = [item.name for item in report.results]
    assert names[0] == "reconnaissance"
    skipped = {item.attack: item.reason for item in report.skipped}
    assert skipped["symbolic"] == "not implemented in this phase"


def test_hypotheses_do_not_cross_targets():
    hyps = generate_from_memory(_memory())
    syracuse = [item for item in hyps if item.source_target == "syracuse"]
    packet = BlindPacket(spec_name="rplus", dimension=1)
    assert_hypotheses_not_injected(packet, syracuse)
    payload = packet.attack_payload()
    blob = repr(payload)
    for item in syracuse:
        assert item.id not in blob
        assert item.statement not in blob
    memory = _memory()
    remember_hypotheses(memory, syracuse[:1])
    restored = ResearchMemory.from_dict(memory.as_dict())
    stored = restored.hypotheses()
    assert stored
    assert stored[0].source_target == "syracuse"
    other = BlindPacket(spec_name="hidden_congruence_a", dimension=1)
    assert_hypotheses_not_injected(other, stored)


def test_foreign_hypothesis_cannot_be_a_predicate_for_another_spec():
    hyp = ResearchHypothesis(
        id="hyp:syracuse:loot:latent",
        statement="parameterized family 2^k y = 3x+1",
        target="syracuse",
        source_target="syracuse",
        closest_known_result="accelerated odd-only 3x+1 / Syracuse map",
    )
    packet = BlindPacket(spec_name="two_path_z2", dimension=2)
    assert_hypotheses_not_injected(packet, (hyp,))
    adapter_source = "class TwoPathZ2Spec:\n    dimension = 2\n"
    assert hyp.statement not in adapter_source
    assert "KNOWN" not in packet.attack_payload()
