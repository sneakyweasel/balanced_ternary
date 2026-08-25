"""Multiplicative residual universality under ``λ·D(s+∏ d_i)``."""

from __future__ import annotations

from research.open_problems import get_problem
from research.multiplicative_residual.discovery import (
    doubled_product_report,
    pair_controls,
    product_raw,
    product_step,
    raw_fibers,
    raw_image,
    separator_equal_raw,
    three_trit_report,
    triple_controls,
    two_trit_report,
    universality_fingerprint,
)
from research.multiplicative_residual.lean_export import (
    CLOSURE_THEOREM,
    export_multiplicative_targets,
    closure_is_exact_size,
)
from research.multiplicative_residual.planner import (
    CLOSURE_HYPOTHESIS,
    FACTOR_COUNT_HYPOTHESIS,
    THREE_STATE_HYPOTHESIS,
    plan_multiplicative_residual,
    plan_product_pair,
)
from research.multiplicative_residual.problem import PROBLEM
from research.multiplicative_residual.records import RECORD_DIR, write_records
from research.multiplicative_residual.spec import (
    ProductResidualSpec,
    minimized_state_count,
    product_spec,
    raw_state_count,
)
from research.signed_digit_residual.discovery import signed_step
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_problem_is_registered():
    assert get_problem("multiplicative_residual") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/multiplicative_residual.md",)


def test_two_trit_raw_quotient_and_u1_match():
    controls = pair_controls()
    assert len(controls) == 9
    assert raw_image(controls) == frozenset({-1, 0, 1})
    fibers = raw_fibers(controls)
    assert set(fibers[1]) == {(1, 1), (-1, -1)}
    assert set(fibers[-1]) == {(1, -1), (-1, 1)}
    assert len(fibers[0]) == 5
    for gain in (1, 2, 3):
        report = two_trit_report(gain)
        assert report["raw_controls"] == 9
        assert report["raw_contribution_count"] == 3
        assert report["reachable"] == (0,)
        assert report["mealy"] == 1
        assert report["control_output_classes_at_0"] == 3
        assert report["u1_reachable"] == (0,)
        assert report["separator"] is None
        for d1, d2 in controls:
            assert product_step(0, (d1, d2), gain) == signed_step(0, d1 * d2, gain)


def test_three_trit_matches_two_trit():
    assert len(triple_controls()) == 27
    assert raw_image(triple_controls()) == frozenset({-1, 0, 1})
    for gain in (1, 2, 3):
        report = three_trit_report(gain)
        assert report["matches_two_trit_reachable"] is True
        assert report["reachable"] == (0,)
        assert report["mealy"] == 1
        assert report["separator"] is None


def test_doubled_product_follows_raw_alphabet_not_factor_count():
    finite = doubled_product_report(1)
    assert finite["raw_contributions"] == (-2, 0, 2)
    assert finite["reachable"] == (-1, 0, 1)
    assert finite["classification"] == "EXACT FINITE"
    assert finite["separator"] is None
    gain2 = doubled_product_report(2)
    assert gain2["classification"] == "EXACT FINITE"
    infinite = doubled_product_report(3)
    assert infinite["classification"] == "EXACT INFINITE"
    assert infinite["unbounded_witness"] is True
    assert product_raw((1, 1)) == 1
    assert product_step(0, (1, 1), gain=3, scale=2) == (3, -1)


def test_no_equal_raw_separator_on_a_window():
    assert separator_equal_raw(pair_controls(), 1, states=range(-8, 9)) is None
    assert separator_equal_raw(triple_controls(), 1, states=range(-4, 5)) is None
    assert universality_fingerprint()["universality"] is True


def test_spec_and_planner():
    spec = product_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is None
    assert spec.transition((0,), (1, 1), spec.initial_phase()) == (0,)
    assert spec.output((0,), (1, 1)) == 1
    assert spec.output((0,), (1, -1)) == -1
    assert raw_state_count() == 1
    assert minimized_state_count() == 1
    assert ProductResidualSpec().name == "multiplicative_residual"
    report = plan_multiplicative_residual(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 1)
    hyp = next(item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id)
    assert hyp.status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == FACTOR_COUNT_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == THREE_STATE_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    three = plan_product_pair(3, remaining=4)
    closure = next(item for item in three.results if item.name == "closure")
    assert closure.status is AttackStatus.SUPPORTED
    assert closure.evidence.get("union_size") == 1


def test_export_links_lean_and_records(tmp_path):
    report = plan_multiplicative_residual(4)
    targets = export_multiplicative_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "multiplicative_residual"
    assert (RECORD_DIR / "closure.yaml").is_file()
    assert (RECORD_DIR / "family.yaml").is_file()
