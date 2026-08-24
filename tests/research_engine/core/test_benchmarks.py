"""Five synthetic systems with known behavior; none of them is Ostrowski |L_0|."""

from __future__ import annotations

import pytest

from research_engine.attacks.block import BlockKind
from research_engine.attacks.result import AttackStatus
from research_engine.benchmarks.pipeline import live_infinite_hypothesis, run_all_benchmarks, run_benchmark
from research_engine.benchmarks.systems import affine_expand, affine_triple
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.negative import NegativeKnowledge
from research_engine.planner.orchestrator import promote_if_legal
from research_engine.attacks.modular import coordinate_forcing_gcds


def _by_name(report, name: str):
    return next(item for item in report.results if item.name == name)


def test_benchmark_a_finite_live_closure():
    report = run_benchmark("A")
    recon = _by_name(report, "reconnaissance")
    assert recon.scope == SearchScope.BOUNDED
    assert recon.status == AttackStatus.OBSERVATION
    assert recon.evidence["union_size"] == 1
    assert recon.evidence["complete"] is True
    affine = _by_name(report, "affine")
    assert affine.status == AttackStatus.OBSERVATION
    modular = _by_name(report, "modular")
    assert modular.status == AttackStatus.SUPPORTED
    block = _by_name(report, "block")
    assert block.evidence["block_kind"] == BlockKind.ORIGIN_RESET.value


def test_benchmark_b_infinite_translate_stays_bounded_observation():
    ledger = ResearchLedger()
    ledger.add_hypothesis(live_infinite_hypothesis("benchmark_infinite_translate"))
    report = run_benchmark("B", ledger)
    recon = _by_name(report, "reconnaissance")
    assert recon.scope == SearchScope.BOUNDED
    assert recon.evidence["complete"] is False
    assert recon.evidence["union_size"] == 9
    assert recon.kind == ClaimKind.LIVE_SLICE
    hyp = ledger.get("benchmark_infinite_translate_live_infinite")
    assert hyp.status is HypothesisStatus.OPEN
    with pytest.raises(LedgerError):
        promote_if_legal(ledger, hyp.id, recon)
    assert ledger.get(hyp.id).status is HypothesisStatus.OPEN


def test_benchmark_c_infinite_words_finite_terminals():
    report = run_benchmark("C")
    recon = _by_name(report, "reconnaissance")
    assert recon.evidence["complete"] is True
    assert recon.evidence["union_size"] == 1
    assert recon.evidence["terminal_image_size"] == 1
    blocked = {item.id for item in report.blocked_jumps}
    assert "unbounded_words_not_unbounded_terminals" in blocked
    knowledge = NegativeKnowledge()
    assert knowledge.forbids("unbounded_accepted_words", "unbounded_terminals") is not None


def test_benchmark_d_modular_forcing_is_a_map_law():
    report = run_benchmark("D")
    modular = _by_name(report, "modular")
    assert modular.status == AttackStatus.SUPPORTED
    assert modular.kind == ClaimKind.REACHABLE
    assert modular.scope == SearchScope.EXACT
    assert coordinate_forcing_gcds(affine_triple()) == (3,)
    assert modular.kind != ClaimKind.LIVE


def test_benchmark_e_expanding_trajectories_leave_the_live_region():
    report = run_benchmark("E")
    recon = _by_name(report, "reconnaissance")
    assert recon.evidence["union_size"] == 1
    assert recon.evidence["rejected_images"] >= 1
    block = _by_name(report, "block")
    assert block.evidence["block_kind"] == BlockKind.ORIGIN_RESET.value
    assert affine_expand().A == ((2,),)
    assert recon.kind == ClaimKind.LIVE_SLICE


def test_all_five_benchmarks_run_and_never_support_exact_live():
    reports = run_all_benchmarks()
    assert set(reports) == {"A", "B", "C", "D", "E"}
    for letter, report in reports.items():
        del letter
        for result in report.results:
            if result.kind is ClaimKind.LIVE:
                raise AssertionError("benchmark pipeline emitted a LIVE claim")
            if result.status is AttackStatus.SUPPORTED:
                assert result.kind is not ClaimKind.LIVE
                assert result.scope is SearchScope.EXACT
        assert "spectral" in {item.attack for item in report.skipped}
