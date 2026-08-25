"""Three-digit integer jet of expanding ``T``."""

from __future__ import annotations

from bt.calculus.integral import I
from bt.calculus.jets import integer_jet
from research.balanced_ternary.expanding_d import expanding_d, sample_range
from research.balanced_ternary.expanding_j2 import j2
from research.balanced_ternary.expanding_j3 import (
    JET3_STATES,
    discovery_report,
    j1_insufficient_witness,
    j2_insufficient_for_next,
    j3,
    j3_from_j2,
    j3_orbit,
    j3_transition,
    predicted_j3_orbit,
    t_image,
)
from research.balanced_ternary.expanding_j3_spec import (
    JET3_REGION,
    T_CONTROL,
    ExpandingJ3Spec,
    current_output_count,
    expanding_j3_spec,
    image_state_count,
    minimized_next_output_count,
    raw_state_count,
)
from research.balanced_ternary.lean_export import closure_is_exact_size
from research.balanced_ternary.planner import plan_expanding_j3, plan_j3_gain
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_j3_is_existing_integer_jet():
    for n in sample_range(20):
        assert j3(n) == integer_jet(n, 3)
        a, b, _c = j3(n)
        assert j3(I(1, n)) == (1, a, b)


def test_exact_jet_map_factors_through_j2_and_discards_c():
    for n in sample_range(40):
        a, b, c = j3(n)
        nxt = j3(expanding_d(n))
        assert nxt == j3_transition((a, b, c))
        assert nxt == (-a, a, b)
        assert nxt == j3_from_j2((a, b))
        assert nxt[:2] == j2(expanding_d(n))
        assert j3_orbit(n, 6) == predicted_j3_orbit(n, 6)
    assert j3(1) == (1, 0, 0)
    assert j3(4) == (1, 1, 0)
    assert j3(10) == (1, 0, 1)
    assert j3(expanding_d(1)) == (-1, 1, 0)
    assert j3(expanding_d(4)) == (-1, 1, 1)
    assert j3(expanding_d(10)) == (-1, 1, 0)
    assert j1_insufficient_witness((1, 4)) == (1, 4)
    assert j2_insufficient_for_next(sample_range(40)) is None
    assert j2(1) == j2(10)
    assert j3(1) != j3(10)


def test_discovery_j3_is_closed_twenty_seven_classes():
    report = discovery_report(limit=80, length=6)
    assert report["status"] == "OBSERVATION"
    assert report["observed_j3_count"] == 27
    assert report["raw_j3_count"] == 27
    assert report["predicted_matches_sample"] is True
    assert report["j1_insufficient"] is not None
    assert report["j2_insufficient_for_next"] is None
    assert t_image() == {
        (-a, a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)
    }


def test_perturbation_keeps_second_digit_at_order_three():
    assert j3_transition((1, -1, 1), 1) == (-1, 1, -1)
    assert j3_transition((1, -1, 1), 2) == (1, 0, -1)
    assert j3_transition((1, -1, 1), 3) == (0, 0, -1)
    for n in sample_range(20):
        a, b, _c = j3(n)
        assert j3(expanding_d(n, 2)) == (a, 0, b)
        assert j3(expanding_d(n, 3)) == (0, 0, b)
    for gain in (1, 2, 3):
        report = plan_j3_gain(gain, remaining=4)
        closure = next(item for item in report.results if item.name == "closure")
        assert closure.status is AttackStatus.SUPPORTED
        assert closure.evidence["union_size"] == 27
        assert closure.evidence["complete"] is True
    assert image_state_count(1) == 9
    assert image_state_count(2) == 9
    assert image_state_count(3) == 3


def test_spec_closure_and_mealy_split():
    spec = expanding_j3_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is None
    assert spec.dimension == 3
    assert spec.transition((1, 0, 1), T_CONTROL, spec.initial_phase()) == (-1, 1, 0)
    assert spec.transition((1, 0, 1), ("I", -1), spec.initial_phase()) == (-1, 1, 0)
    assert raw_state_count() == 27
    assert current_output_count() == 27
    assert image_state_count() == 9
    assert minimized_next_output_count() == 9
    assert set(JET3_REGION) == set(JET3_STATES)


def test_planner_certifies_twenty_seven_not_horizon():
    report = plan_expanding_j3(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 27)
    hyp = next(item for item in report.hypotheses if item.id == "expanding_j3_closure")
    assert hyp.status is HypothesisStatus.SUPPORTED
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    assert ExpandingJ3Spec().name == "expanding_j3"
