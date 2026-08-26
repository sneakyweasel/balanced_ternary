"""v2.3 Phase 4: EXISTS_PATH ≠ ALL_PATHS, relation view, frozen flood order."""

from __future__ import annotations

from research.linear_constraint_loops.spec import decrement_spec, sum_strip_spec
from research.linear_constraint_loops.synthetics import (
    dual_decrement_spec,
    stay_or_decrement_spec,
    two_affine_spec,
)
from research_engine.attacks.piecewise_affine import PiecewiseAffineCensusAttack
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.hidden_piecewise import HiddenPowerClearDSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.law import ENGINE_LAW_VERSION
from research_engine.memory.retrieval import assert_hypotheses_not_injected
from research_engine.memory.store import ResearchMemory
from research_engine.memory.types import BlindPacket, NoveltyStatus
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.quantifiers import (
    ENGINE_QUANTIFIER_VERSION,
    PathQuantifier,
    PathStatus,
    analyze,
    certified_on_window_is_not_z_theorem,
    existential_cycle_is_not_all_paths_cycle,
    hypotheses_from_report,
    live_hypothesis_unpromoted,
    no_path_found_is_not_nonexistence,
    truncation_is_unknown_not_refuted,
)
from research_engine.reasoning import ENGINE_REASONING_VERSION
from research_engine.strategy import (
    ENGINE_STRATEGY_VERSION,
    QUANTIFIER_PROBE_CHAIN,
    ResearchGoal,
    ResearchHypothesis,
    StrategyPlanner,
    freeze_attack_order,
    select_chain,
)
from research_engine.strategy.types import ObligationKind, ProofObligation
from tests.research_engine.core.test_planner import CountdownSpec


def _claim(report, name: str):
    item = report.claim(name)
    assert item is not None
    return item


def test_quantifier_version_and_frozen_order():
    assert ENGINE_QUANTIFIER_VERSION == "0.2.6"
    assert ENGINE_STRATEGY_VERSION == "0.2.3"
    assert ENGINE_REASONING_VERSION == "0.2.4"
    assert ENGINE_LAW_VERSION == "0.2.5"
    assert freeze_attack_order() == DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "quantifier_probe" not in DEFAULT_ATTACK_ORDER
    assert QUANTIFIER_PROBE_CHAIN.attacks == ()
    assert QUANTIFIER_PROBE_CHAIN.id not in DEFAULT_ATTACK_ORDER


def test_stay_or_decrement_exists_is_not_all_paths():
    spec = stay_or_decrement_spec()
    ctx = spec.attack_context()
    report = analyze(spec, ctx)
    exists = _claim(report, "existential_cycle")
    all_paths = _claim(report, "all_paths_cycle")
    terminate = _claim(report, "universal_termination")
    assert exists.quantifier is PathQuantifier.EXISTS_PATH
    assert exists.status is PathStatus.EXISTENTIAL_WITNESS
    assert exists.witness
    assert all_paths.status is PathStatus.UNKNOWN
    assert all_paths.status is not PathStatus.CERTIFIED_ON_WINDOW
    assert terminate.status is PathStatus.REFUTED
    assert report.census_skipped
    assert report.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
    assert exists.source_target == spec.name
    assert existential_cycle_is_not_all_paths_cycle(report)
    flood = PiecewiseAffineCensusAttack().run(spec, ctx)
    assert flood.status is AttackStatus.INAPPLICABLE
    hyps = hypotheses_from_report(report)
    assert any(item.current_status.value == "SEARCH_SUPPORTED" for item in hyps)
    assert any(item.current_status.value == "REFUTED" for item in hyps)
    assert all("Carelli" not in item.statement for item in hyps)
    assert all("length" not in item.statement.lower() or "2" not in item.statement for item in hyps)


def test_two_affine_second_branching_target():
    spec = two_affine_spec()
    ctx = spec.attack_context()
    report = analyze(spec, ctx)
    exists = _claim(report, "existential_cycle")
    assert exists.status is PathStatus.EXISTENTIAL_WITNESS
    assert _claim(report, "all_paths_cycle").status is PathStatus.UNKNOWN
    assert _claim(report, "universal_termination").status is PathStatus.REFUTED
    assert report.census_skipped
    assert report.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
    flood = PiecewiseAffineCensusAttack().run(spec, ctx)
    assert flood.status is AttackStatus.INAPPLICABLE
    assert PiecewiseAffineCensusAttack().applicable(spec, ctx) is False


def test_dual_decrement_window_versus_truncation():
    spec = dual_decrement_spec()
    ctx = spec.attack_context()
    small = tuple(range(0, 8))
    certified = analyze(spec, ctx, window=small, max_depth=24)
    term = _claim(certified, "universal_termination")
    assert term.status is PathStatus.CERTIFIED_ON_WINDOW
    assert _claim(certified, "existential_cycle").status is PathStatus.NO_PATH_FOUND
    assert no_path_found_is_not_nonexistence(certified)
    assert certified_on_window_is_not_z_theorem(certified)
    truncated = analyze(spec, ctx, window=small, max_depth=1)
    trunc_term = _claim(truncated, "universal_termination")
    assert trunc_term.status is PathStatus.UNKNOWN
    assert trunc_term.status is not PathStatus.REFUTED
    assert truncation_is_unknown_not_refuted(truncated)
    hyps = hypotheses_from_report(certified)
    assert all(item.current_status.value != "PROVED" for item in hyps)
    assert all(item.current_status.value != "LEAN_CERTIFIED" for item in hyps)


def test_sum_strip_is_parked_diagnostic_not_a_theorem():
    spec = sum_strip_spec()
    ctx = spec.attack_context()
    report = analyze(spec, ctx)
    assert _claim(report, "existential_cycle").status is PathStatus.EXISTENTIAL_WITNESS
    assert _claim(report, "universal_termination").status is PathStatus.REFUTED
    assert _claim(report, "all_paths_cycle").status is PathStatus.UNKNOWN
    assert report.census_skipped
    assert report.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
    flood = PiecewiseAffineCensusAttack().run(spec, ctx)
    assert flood.status is AttackStatus.INAPPLICABLE
    blob = " ".join(item.statement for item in hypotheses_from_report(report))
    assert "Carelli" not in blob
    assert "length ≤ 2" not in blob.lower()
    assert "length-<=2" not in blob.lower()


def test_phase1_cycle_exclusion_still_selects_census_without_memory():
    spec = HiddenPowerClearDSpec()
    plan = select_chain(spec, ResearchGoal.CYCLE_EXCLUSION)
    assert plan.chain.id == "census_obstruction"


def test_phase2_termination_still_selects_global_inductive():
    spec = decrement_spec()
    plan = select_chain(spec, ResearchGoal.TERMINATION)
    assert plan.chain.id == "global_inductive"


def test_strategy_selects_quantifier_probe_when_memory_has_quantifier():
    spec = stay_or_decrement_spec()
    memory = ResearchMemory()
    memory.add_hypothesis(
        ResearchHypothesis(
            id="hyp:quant:seed",
            statement="exists a legal cycle",
            target=spec.name,
            source_target=spec.name,
            cluster_id="branching_quantifier",
            proof_obligations=(
                ProofObligation(kind=ObligationKind.EXISTS_PATH, statement="Need: EXISTS_PATH"),
            ),
        )
    )
    plan = select_chain(spec, ResearchGoal.CYCLE_EXCLUSION, memory)
    assert plan.chain.id == "quantifier_probe"
    report = StrategyPlanner().run(
        spec,
        spec.attack_context(),
        goal=ResearchGoal.CYCLE_EXCLUSION,
        memory=memory,
    )
    assert report.attempted_chains == ("quantifier_probe",)
    assert report.results == ()
    assert report.quantifiers is not None
    assert any(item.current_status.value == "SEARCH_SUPPORTED" for item in report.hypotheses)


def test_session_live_hypothesis_stays_unpromoted():
    hyp = Hypothesis(
        id="live_infinite",
        statement="the live set is infinite",
        kind=ClaimKind.LIVE,
        intended_scope=SearchScope.EXACT,
        status=HypothesisStatus.OPEN,
    )
    assert live_hypothesis_unpromoted(hyp)
    report = analyze(CountdownSpec(), AttackContext(live_only=True, max_steps=4, max_states=16))
    assert all(item.status is not PathStatus.CERTIFIED_ON_WINDOW or "Z-theorem" in item.statement for item in report.claims)
    assert hyp.status is HypothesisStatus.OPEN


def test_memory_json_without_quantifier_fields_still_loads():
    memory = ResearchMemory.load_historical()
    dumped = memory.as_dict()
    assert "quantifiers" not in dumped
    restored = ResearchMemory.from_dict({"experiments": dumped["experiments"]})
    assert restored.hypotheses() == ()
    assert len(restored.experiments) == len(memory.experiments)


def test_witnesses_do_not_cross_targets():
    spec = stay_or_decrement_spec()
    report = analyze(spec, spec.attack_context())
    hyps = hypotheses_from_report(report)
    assert hyps
    packet = BlindPacket(spec_name="two_path_z2", dimension=2)
    assert_hypotheses_not_injected(packet, hyps)
    blob = repr(packet.attack_payload())
    for item in hyps:
        assert item.id not in blob
        assert item.source_target == "hidden_nondet_stay_or_decrement"
