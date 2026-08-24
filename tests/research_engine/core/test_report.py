"""Planner text reports do not promote LIVE infinitude."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.pipeline import load_benchmark, run_benchmark
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import run_named_attack
from research_engine.report import DISCLAIMER, format_planner_report, format_target_report
from research_engine.verification.targets import targets_from_report


def test_benchmark_b_report_stays_bounded_live_slice():
    report = run_benchmark("B")
    text = format_planner_report(report, problem="B")
    assert DISCLAIMER in text
    assert "LIVE_SLICE" in text
    assert "BOUNDED" in text
    assert "SUPPORTED EXACT LIVE" not in text
    assert "sorry" not in text.lower()
    assert "admit" not in text.lower()


def test_benchmark_d_report_targets_are_exportable_map_laws():
    report = run_benchmark("D")
    targets = targets_from_report(report, problem="benchmark_D")
    text = format_target_report(targets)
    assert "exportable: true" in text
    assert "benchmark_D_modular" in text
    assert "sorry" not in text.lower()
    modular = next(item for item in report.results if item.name == "modular")
    assert modular.status is AttackStatus.SUPPORTED
    assert modular.scope is SearchScope.EXACT
    assert modular.kind is ClaimKind.REACHABLE


def test_named_attack_deferred_symbolic_is_inapplicable():
    spec, context = load_benchmark("D")
    result = run_named_attack("symbolic", spec, context)
    assert result.status is AttackStatus.INAPPLICABLE
    spectral = run_named_attack("spectral", spec, AttackContext(affine=context.affine))
    assert spectral.status is AttackStatus.OBSERVATION
    assert spectral.kind is ClaimKind.REACHABLE
    assert spectral.kind is not ClaimKind.LIVE
    modular = run_named_attack("modular", spec, AttackContext(affine=context.affine))
    assert modular.status is AttackStatus.SUPPORTED
