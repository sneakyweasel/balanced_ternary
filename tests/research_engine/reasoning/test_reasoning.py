"""v2.3 Phase 2: inductive/ranking certificates, evidence discipline, frozen flood order."""

from __future__ import annotations

from research.euclidean_quotient.spec import euclidean_spec
from research.linear_constraint_loops.spec import decrement_spec, rplus_spec
from research.positivity_lrs.spec import early_negative_spec
from research.skolem_lrs.spec import zero_small_spec
from research.switching_affine_z2_origin.spec import TwoPathZ2Spec
from research_engine.attacks.result import AttackContext
from research_engine.benchmarks.hidden_piecewise import HiddenInvolutionESpec, HiddenPowerClearDSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.memory.retrieval import assert_hypotheses_not_injected
from research_engine.memory.store import ResearchMemory
from research_engine.memory.types import BlindPacket, NoveltyStatus
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.reasoning import (
    ENGINE_REASONING_VERSION,
    EvidenceState,
    Region,
    RegionForm,
    analyze,
    certify_invariant,
    clamp_universal,
    from_closure,
    hypotheses_from_report,
    live_hypothesis_unpromoted,
)
from research_engine.strategy import (
    ENGINE_STRATEGY_VERSION,
    GLOBAL_INDUCTIVE_CHAIN,
    ResearchGoal,
    StrategyPlanner,
    freeze_attack_order,
    select_chain,
)
from tests.research_engine.core.test_planner import CountdownSpec

_FORBIDDEN_UNIVERSAL = EvidenceState.UNIVERSAL_THEOREM


def _evidence(report) -> set[EvidenceState]:
    found: set[EvidenceState] = set()
    if report.invariant is not None:
        found.add(report.invariant.evidence)
    if report.ranking is not None:
        found.add(report.ranking.evidence)
    if report.closure_complete:
        found.add(from_closure(complete=True))
    return found


def test_reasoning_version_and_frozen_flood_order():
    assert ENGINE_REASONING_VERSION == "0.2.4"
    assert ENGINE_STRATEGY_VERSION == "0.2.3"
    assert freeze_attack_order() == DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "global_inductive" not in DEFAULT_ATTACK_ORDER
    assert GLOBAL_INDUCTIVE_CHAIN.attacks == ()


def test_two_path_z2_nonnegative_orthant_is_known_inductive():
    spec = TwoPathZ2Spec()
    report = analyze(spec, spec.attack_context())
    assert report.invariant is not None
    assert report.invariant.evidence is EvidenceState.INDUCTIVE_CERTIFIED
    assert report.invariant.region.form is RegionForm.SIGN_ORTHANT
    assert report.invariant.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
    assert report.invariant.source_target == "two_path_z2"
    assert report.invariant.evidence is not _FORBIDDEN_UNIVERSAL
    hyps = hypotheses_from_report(report)
    assert any(item.current_status.value == "PROOF_READY" for item in hyps)
    assert all(item.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY for item in hyps)


def test_decrement_ranking_is_known_certified():
    spec = decrement_spec()
    report = analyze(spec, spec.attack_context())
    assert report.invariant is not None
    assert report.invariant.evidence is EvidenceState.INDUCTIVE_CERTIFIED
    assert report.ranking is not None
    assert report.ranking.evidence is EvidenceState.RANKING_CERTIFIED
    assert report.ranking.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
    assert report.ranking.source_target == "slc_decrement"
    assert report.ranking.evidence is not _FORBIDDEN_UNIVERSAL


def test_euclidean_is_not_a_universal_theorem():
    spec = euclidean_spec()
    report = analyze(spec, spec.attack_context())
    assert _FORBIDDEN_UNIVERSAL not in _evidence(report)
    if report.invariant is not None:
        assert report.invariant.universal_domain is False


def test_hidden_involution_finite_set_is_not_universal():
    spec = HiddenInvolutionESpec()
    report = analyze(spec, spec.attack_context())
    assert _FORBIDDEN_UNIVERSAL not in _evidence(report)
    finite = Region(
        form=RegionForm.FINITE_SET,
        parameters={"states": ((0,), (1,))},
        dimension=1,
    )
    cert = certify_invariant(spec, finite, spec.attack_context(), observed=((0,), (1,)), closure_complete=True)
    assert cert.evidence is EvidenceState.FINITE_EXACT
    assert cert.evidence is not _FORBIDDEN_UNIVERSAL


def test_cluster_replays_are_not_universal_theorems():
    for spec in (rplus_spec(), zero_small_spec(), early_negative_spec()):
        report = analyze(spec, spec.attack_context())
        assert _FORBIDDEN_UNIVERSAL not in _evidence(report)
        if report.invariant is not None:
            assert report.invariant.universal_domain is False
            assert report.invariant.evidence is not _FORBIDDEN_UNIVERSAL
        if report.ranking is not None:
            assert report.ranking.evidence is not _FORBIDDEN_UNIVERSAL


def test_finite_exact_is_never_promoted_to_universal():
    assert from_closure(complete=True) is EvidenceState.FINITE_EXACT
    assert clamp_universal(EvidenceState.UNIVERSAL_THEOREM, universal_domain=False) is EvidenceState.UNKNOWN
    spec = HiddenInvolutionESpec()
    report = analyze(spec, spec.attack_context())
    assert report.invariant is None or report.invariant.evidence is not _FORBIDDEN_UNIVERSAL


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
    assert _FORBIDDEN_UNIVERSAL not in _evidence(report)
    assert hyp.status is HypothesisStatus.OPEN


def test_strategy_selects_global_inductive_for_termination():
    spec = decrement_spec()
    plan = select_chain(spec, ResearchGoal.TERMINATION)
    assert plan.chain.id == "global_inductive"
    report = StrategyPlanner().run(spec, spec.attack_context(), goal=ResearchGoal.TERMINATION)
    assert report.attempted_chains == ("global_inductive",)
    assert report.results == ()
    assert any(
        item.current_status.value == "PROOF_READY" and "V=" in item.statement
        for item in report.hypotheses
    )
    flood_names = list(DEFAULT_ATTACK_ORDER)
    assert [item.name for item in report.results] != flood_names


def test_phase1_cycle_exclusion_still_selects_census():
    spec = HiddenPowerClearDSpec()
    plan = select_chain(spec, ResearchGoal.CYCLE_EXCLUSION)
    assert plan.chain.id == "census_obstruction"


def test_memory_json_without_reasoning_fields_still_loads():
    memory = ResearchMemory.load_historical()
    dumped = memory.as_dict()
    assert "reasoning" not in dumped
    restored = ResearchMemory.from_dict({"experiments": dumped["experiments"]})
    assert restored.hypotheses() == ()
    assert len(restored.experiments) == len(memory.experiments)


def test_certificates_do_not_cross_targets():
    spec = TwoPathZ2Spec()
    report = analyze(spec, spec.attack_context())
    hyps = hypotheses_from_report(report)
    assert hyps
    packet = BlindPacket(spec_name="rplus", dimension=1)
    assert_hypotheses_not_injected(packet, hyps)
    blob = repr(packet.attack_payload())
    for item in hyps:
        assert item.id not in blob
        assert item.source_target == "two_path_z2"
