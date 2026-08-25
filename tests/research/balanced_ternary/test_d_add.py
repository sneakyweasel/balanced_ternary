"""Discovery of the ``D(x+y)`` residual."""

from __future__ import annotations

from bt.arithmetic import add
from bt.calculus.derivative import D
from bt.calculus.differential import D_of_sum, add_correction
from bt.calculus.jets import integer_jet
from bt.representation import digits, encode
from research.balanced_ternary.d_add import (
    TRITS,
    collisions,
    correction,
    discovery_report,
    pack_digits,
    r_digit_pair,
    r_lsd_sum,
    residual_collision,
    sample_range,
    step,
    stream_sum,
    streaming_reachable,
)
from research.balanced_ternary.d_add_spec import (
    DAddResidualSpec,
    d_add_spec,
    minimized_state_count,
    raw_state_count,
)
from research.balanced_ternary.lean_export import closure_is_exact_size
from research.balanced_ternary.planner import plan_d_add, plan_d_add_bound
from research.balanced_ternary.spec import emit as doubled_emit
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_naive_factorization_collides_and_lsd_sum_is_not_enough():
    values = sample_range(8)
    coll = collisions(values)
    assert (0, 0) in coll
    hit = residual_collision(values, r_lsd_sum)
    assert hit is not None
    left, right = hit
    assert (D(left[0]), D(left[1]), r_lsd_sum(*left)) == (
        D(right[0]),
        D(right[1]),
        r_lsd_sum(*right),
    )
    assert D(left[0] + left[1]) != D(right[0] + right[1])
    assert residual_collision(values, r_digit_pair) is None
    assert residual_collision(values, correction) is None
    assert D(1 + 1) == 1
    assert D(0 + (-1)) == 0
    assert D(1) == D(0) == D(-1) == 0
    assert r_lsd_sum(1, 1) == r_lsd_sum(0, -1) == -1


def test_discovered_correction_is_d_of_digit_sum():
    for x in sample_range(15):
        for y in sample_range(15):
            ax, ay = integer_jet(x, 1)[0], integer_jet(y, 1)[0]
            assert correction(x, y) == D(ax + ay)
            assert correction(x, y) == add_correction(x, y)[1]
            assert D(x + y) == D(x) + D(y) + correction(x, y)
            assert D(x + y) == D_of_sum(x, y)


def test_streaming_matches_integer_sum_and_phase0_diagonal():
    for x in sample_range(10):
        for y in sample_range(10):
            streamed = stream_sum(x, y)
            assert pack_digits(streamed) == x + y
            assert pack_digits(digits(add(encode(x), encode(y)))) == x + y
    for residual in TRITS:
        for digit in TRITS:
            nxt, out = step(residual, digit, digit)
            d_nxt, d_out = doubled_emit(residual, digit)
            assert (nxt, out) == (d_nxt, d_out)


def test_discovery_report_finds_three_state_residual():
    report = discovery_report(limit=10)
    assert report["status"] == "OBSERVATION"
    assert report["correction_values"] == (-1, 0, 1)
    assert report["streaming_reachable"] == (-1, 0, 1)
    assert report["digit_pair_separates"] is True
    assert report["correction_separates"] is True
    assert report["lsd_sum_collision"] is not None


def test_spec_closure_and_mealy():
    spec = d_add_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is None
    assert spec.dimension == 1
    assert spec.transition((0,), (1, 1), spec.initial_phase()) == (1,)
    assert spec.output((0,), (1, 1)) == -1
    assert raw_state_count(1) == 3
    assert minimized_state_count(1) == 3
    assert streaming_reachable((-2, -1, 0, 1, 2)) == frozenset(range(-2, 3))


def test_planner_certifies_three_and_perturbation_widens_the_box():
    report = plan_d_add(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 3)
    hyp = next(item for item in report.hypotheses if item.id == "d_add_residual_closure")
    assert hyp.status is HypothesisStatus.SUPPORTED
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    assert DAddResidualSpec().name == "d_add"
    wide = plan_d_add_bound(2, remaining=4)
    closure = next(item for item in wide.results if item.name == "closure")
    assert closure.status is AttackStatus.SUPPORTED
    assert closure.evidence["union_size"] == 5
    assert closure.evidence["complete"] is True
    assert raw_state_count(2) == 5
    assert minimized_state_count(2) == 5
