"""Two-digit integer jet of expanding ``T``."""

from __future__ import annotations

from bt.calculus.integral import I
from bt.calculus.jets import integer_jet
from research.balanced_ternary.expanding_d import expanding_d, sample_range
from research.balanced_ternary.expanding_j2 import (
    JET2_STATES,
    discovery_report,
    j2,
    j2_orbit,
    j2_transition,
    predicted_j2_orbit,
    second_digit_affects_next_j2,
    t_image,
    third_digit_separates,
)
from research.balanced_ternary.expanding_j2_spec import (
    JET2_REGION,
    T_CONTROL,
    ExpandingJ2Spec,
    current_output_count,
    expanding_j2_spec,
    image_state_count,
    minimized_next_output_count,
    raw_state_count,
)
from research.balanced_ternary.lean_export import closure_is_exact_size
from research.balanced_ternary.planner import plan_expanding_j2, plan_j2_gain
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_j2_is_existing_integer_jet():
    for n in sample_range(20):
        assert j2(n) == integer_jet(n, 2)
        assert j2(I(1, n)) == (1, j2(n)[0])


def test_exact_jet_map_ignores_second_digit_and_third():
    for n in sample_range(30):
        a, b = j2(n)
        assert j2(expanding_d(n)) == j2_transition((a, b))
        assert j2(expanding_d(n)) == (-a, a)
        assert j2_orbit(n, 6) == predicted_j2_orbit(n, 6)
    assert j2(1) == (1, 0)
    assert j2(4) == (1, 1)
    assert j2(expanding_d(1)) == j2(expanding_d(4)) == (-1, 1)
    assert j2(1) == j2(10)
    assert integer_jet(1, 3) != integer_jet(10, 3)
    assert j2_orbit(1, 8) == j2_orbit(10, 8)


def test_discovery_j2_is_closed_nine_classes():
    report = discovery_report(limit=40, length=8)
    assert report["status"] == "OBSERVATION"
    assert report["class_count"] == 9
    assert report["observed_j2_count"] == 9
    assert report["predicted_matches_sample"] is True
    assert report["third_digit_separates"] is None
    assert report["second_digit_affects_next"] is None
    assert third_digit_separates(sample_range(40), 8) is None
    assert second_digit_affects_next_j2(sample_range(40)) is None
    assert t_image() == {(-1, 1), (0, 0), (1, -1)}


def test_perturbation_visible_at_order_two():
    assert j2_transition((1, -1), 1) == (-1, 1)
    assert j2_transition((1, -1), 2) == (1, 0)
    assert j2_transition((1, -1), 3) == (0, 0)
    for n in sample_range(20):
        a, _b = j2(n)
        assert j2(expanding_d(n, 2)) == (a, 0)
        assert j2(expanding_d(n, 3)) == (0, 0)
    for gain in (1, 2, 3):
        report = plan_j2_gain(gain, remaining=4)
        closure = next(item for item in report.results if item.name == "closure")
        assert closure.status is AttackStatus.SUPPORTED
        assert closure.evidence["union_size"] == 9
        assert closure.evidence["complete"] is True
    assert image_state_count(1) == 3
    assert image_state_count(2) == 3
    assert image_state_count(3) == 1


def test_spec_closure_and_mealy_split():
    spec = expanding_j2_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is None
    assert spec.dimension == 2
    assert spec.transition((1, 0), T_CONTROL, spec.initial_phase()) == (-1, 1)
    assert spec.transition((1, 0), ("I", -1), spec.initial_phase()) == (-1, 1)
    assert raw_state_count() == 9
    assert current_output_count() == 9
    assert image_state_count() == 3
    assert minimized_next_output_count() == 3
    assert set(JET2_REGION) == set(JET2_STATES)


def test_planner_certifies_nine_not_horizon():
    report = plan_expanding_j2(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 9)
    hyp = next(item for item in report.hypotheses if item.id == "expanding_j2_closure")
    assert hyp.status is HypothesisStatus.SUPPORTED
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    assert ExpandingJ2Spec().name == "expanding_j2"
