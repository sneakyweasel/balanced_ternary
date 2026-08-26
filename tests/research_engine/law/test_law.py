"""v2.3 Phase 3: law/domain split, truncated involution, frozen infer_region."""

from __future__ import annotations

from research.linear_constraint_loops.spec import decrement_spec, negation_spec
from research_engine.attacks.piecewise_affine import (
    CensusKind,
    PiecewiseAffineCensusAttack,
    RegionKind,
    infer_region,
    run_piecewise_affine_census,
)
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.hidden_piecewise import HiddenPowerClearDSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.law import (
    ENGINE_LAW_VERSION,
    DomainEvidence,
    LawEvidence,
    analyze,
    hypotheses_from_report,
    live_hypothesis_unpromoted,
    truncated_domain_is_not_certified,
    unresolved_census_stays_unresolved,
)
from research_engine.memory.retrieval import assert_hypotheses_not_injected
from research_engine.memory.store import ResearchMemory
from research_engine.memory.types import BlindPacket, NoveltyStatus
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.reasoning import ENGINE_REASONING_VERSION
from research_engine.strategy import (
    ENGINE_STRATEGY_VERSION,
    LAW_DOMAIN_CHAIN,
    ResearchGoal,
    StrategyPlanner,
    freeze_attack_order,
    select_chain,
)
from tests.research_engine.core.test_planner import CountdownSpec


def _negation_law(report):
    for pair in report.pairs:
        law = pair.law
        if law.q == 1 and law.p == -1 and law.r == 0:
            return pair
    return None


def _decrement_law(report):
    for pair in report.pairs:
        law = pair.law
        if law.q == 1 and law.p == 1 and law.r == -1:
            return pair
    return None


def test_law_version_and_frozen_infer_region_order():
    assert ENGINE_LAW_VERSION == "0.2.5"
    assert ENGINE_STRATEGY_VERSION == "0.2.3"
    assert ENGINE_REASONING_VERSION == "0.2.4"
    assert freeze_attack_order() == DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "law_domain" not in DEFAULT_ATTACK_ORDER
    assert LAW_DOMAIN_CHAIN.attacks == ()
    domain = tuple(range(-8, 9))
    region = infer_region(domain, domain)
    assert region.kind == RegionKind.SIGN.value
    assert region.parameters.get("sign") == "nonneg"


def test_negation_law_certified_with_truncated_domain():
    spec = negation_spec()
    ctx = spec.attack_context()
    report = analyze(spec, ctx)
    pair = _negation_law(report)
    assert pair is not None
    assert pair.law.evidence is LawEvidence.LAW_CERTIFIED
    assert pair.law.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
    assert pair.domain.evidence is DomainEvidence.DOMAIN_TRUNCATED
    assert pair.domain.evidence is not DomainEvidence.DOMAIN_CERTIFIED
    assert pair.domain.truncated
    assert report.census_kind == CensusKind.UNRESOLVED.value
    flood = PiecewiseAffineCensusAttack().run(spec, ctx)
    assert flood.status is AttackStatus.INCONCLUSIVE
    census = run_piecewise_affine_census(spec, ctx)
    assert census.census_kind == CensusKind.UNRESOLVED.value
    assert truncated_domain_is_not_certified(report)
    assert unresolved_census_stays_unresolved(report)
    hyps = hypotheses_from_report(report)
    assert any(item.current_status.value == "PROOF_READY" for item in hyps)
    assert any(
        any(obl.kind.value == "DOMAIN_CERTIFICATION" and obl.status == "OPEN" for obl in item.proof_obligations)
        for item in hyps
    )
    assert all("Carelli" not in item.statement for item in hyps)
    assert all("length" not in item.statement.lower() or "2" not in item.statement for item in hyps)


def test_decrement_law_and_domain_may_both_certify():
    spec = decrement_spec()
    ctx = spec.attack_context()
    report = analyze(spec, ctx)
    pair = _decrement_law(report)
    assert pair is not None
    assert pair.law.evidence is LawEvidence.LAW_CERTIFIED
    assert pair.law.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY
    assert pair.domain.evidence is DomainEvidence.DOMAIN_CERTIFIED
    assert pair.domain.region is not None
    assert pair.domain.region.kind == RegionKind.SIGN.value
    census = run_piecewise_affine_census(spec, ctx)
    assert census.census_kind == CensusKind.FINITE_CENSUS.value


def test_phase1_cycle_exclusion_still_selects_census_without_memory():
    spec = HiddenPowerClearDSpec()
    plan = select_chain(spec, ResearchGoal.CYCLE_EXCLUSION)
    assert plan.chain.id == "census_obstruction"


def test_strategy_selects_law_domain_when_memory_has_domain_inference():
    spec = negation_spec()
    memory = ResearchMemory.load_historical()
    plan = select_chain(spec, ResearchGoal.CYCLE_EXCLUSION, memory)
    assert plan.chain.id == "law_domain"
    report = StrategyPlanner().run(
        spec,
        spec.attack_context(),
        goal=ResearchGoal.CYCLE_EXCLUSION,
        memory=memory,
    )
    assert report.attempted_chains == ("law_domain",)
    assert report.results == ()
    assert report.law is not None
    assert any(item.current_status.value == "PROOF_READY" for item in report.hypotheses)


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
    assert report.census_kind != "UNIVERSAL_THEOREM"
    assert hyp.status is HypothesisStatus.OPEN


def test_memory_json_without_law_fields_still_loads():
    memory = ResearchMemory.load_historical()
    dumped = memory.as_dict()
    assert "law" not in dumped
    restored = ResearchMemory.from_dict({"experiments": dumped["experiments"]})
    assert restored.hypotheses() == ()
    assert len(restored.experiments) == len(memory.experiments)


def test_laws_do_not_cross_targets():
    spec = negation_spec()
    report = analyze(spec, spec.attack_context())
    hyps = hypotheses_from_report(report)
    assert hyps
    packet = BlindPacket(spec_name="two_path_z2", dimension=2)
    assert_hypotheses_not_injected(packet, hyps)
    blob = repr(packet.attack_payload())
    for item in hyps:
        assert item.id not in blob
        assert item.source_target == "slc_negation"
