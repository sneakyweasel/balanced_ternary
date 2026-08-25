"""Signed-digit residual phase transitions."""

from __future__ import annotations

from research.open_problems import get_problem
from research.signed_digit_residual.discovery import (
    DISTINGUISHING_PAIRS,
    alphabet_m,
    asymmetric_perturbation,
    box_leak,
    distinguishing_fingerprint,
    finite_from_origin,
    is_constant_unbounded_family,
    lambda1_invariant_radius_loose,
    lambda1_reachable_radius,
    lyapunov_leak,
    origin_reachable_report,
    r_way_mealy,
    r_way_reachable,
    residual_complexity,
    signed_step,
    trit_sum_values,
)
from research.signed_digit_residual.lean_export import (
    CLOSURE_THEOREM,
    export_signed_digit_targets,
    closure_is_exact_size,
)
from research.signed_digit_residual.planner import (
    CLOSURE_HYPOTHESIS,
    SCALAR_THRESHOLD_HYPOTHESIS,
    plan_signed_digit_pair,
    plan_signed_digit_residual,
)
from research.signed_digit_residual.problem import PROBLEM
from research.signed_digit_residual.records import RECORD_DIR, write_records
from research.signed_digit_residual.spec import (
    SignedDigitResidualSpec,
    minimized_state_count,
    raw_state_count,
    signed_digit_spec,
)
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_problem_is_registered():
    assert get_problem("signed_digit_residual") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/signed_digit_residual.md",)


def test_lambda1_family_separates_box_reachable_and_mealy():
    for bound in (1, 2, 3):
        report = origin_reachable_report(bound, 1)
        radius = lambda1_reachable_radius(bound)
        assert report["classification"] == "EXACT FINITE"
        assert report["reachable"] == tuple(range(-radius, radius + 1))
        assert report["reachable_count"] == residual_complexity(bound)
        assert report["invariant_radius"] == radius
        assert report["mealy"] == residual_complexity(bound)
        assert box_leak(radius, alphabet_m(bound), 1) is None
        if radius > 0:
            assert box_leak(radius - 1, alphabet_m(bound), 1) is not None
        loose = lambda1_invariant_radius_loose(bound)
        assert loose >= radius
        min_abs = (bound + 3) // 2
        assert lyapunov_leak(alphabet_m(bound), 1, min_abs=min_abs, search_radius=20) is None



def test_distinguishing_pairs_are_exact():
    fingerprint = distinguishing_fingerprint()
    expected_reachable = {
        (1, 1): (0,),
        (1, 2): (-1, 0, 1),
        (1, 3): (-1, 0, 1),
        (2, 1): (0,),
        (2, 2): (-2, 0, 2),
        (3, 1): (0,),
    }
    for pair in DISTINGUISHING_PAIRS:
        item = fingerprint[pair]
        assert item["classification"] == "EXACT FINITE"
        assert item["reachable"] == expected_reachable[pair]
        assert item["mealy"] == len(expected_reachable[pair])
        assert finite_from_origin(*pair) is True
    companion = fingerprint[(3, 2)]
    assert companion["classification"] == "EXACT INFINITE"
    assert companion["unbounded_witness"] is True
    assert finite_from_origin(3, 2) is False
    assert is_constant_unbounded_family(2, 3)
    assert signed_step(0, 2, 3) == (3, -1)
    assert signed_step(3, 2, 3) == (6, -1)


def test_gain2_reachable_is_not_the_invariant_interval():
    report = origin_reachable_report(2, 2)
    assert report["reachable"] == (-2, 0, 2)
    assert report["invariant_radius"] == 2
    assert report["mealy"] == 3
    assert box_leak(1, alphabet_m(2), 2) is not None
    assert box_leak(2, alphabet_m(2), 2) is None


def test_r_way_matches_u_r_and_formula():
    for arity in (1, 2, 3, 4):
        assert trit_sum_values(arity) == frozenset(alphabet_m(arity))
        reached = r_way_reachable(arity)
        assert reached is not None
        radius = arity // 2
        assert reached == frozenset(range(-radius, radius + 1))
        assert len(reached) == residual_complexity(arity)
        assert r_way_mealy(arity) == residual_complexity(arity)
    assert r_way_reachable(2) == frozenset({-1, 0, 1})


def test_asymmetric_perturbation_stays_finite():
    report = asymmetric_perturbation()
    assert report["reachable"] == (0, 1)
    assert report["classification"] == "EXACT FINITE"
    assert report["mealy"] == 2


def test_spec_closure_and_mealy():
    spec = signed_digit_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is None
    assert spec.dimension == 1
    assert spec.transition((0,), 2, spec.initial_phase()) == (1,)
    assert spec.output((0,), 2) == -1
    assert raw_state_count(2, 1) == 3
    assert minimized_state_count(2, 1) == 3
    assert SignedDigitResidualSpec().name == "signed_digit_residual"


def test_planner_certifies_three_and_refutes_scalar_threshold():
    report = plan_signed_digit_residual(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 3)
    hyp = next(item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id)
    assert hyp.status is HypothesisStatus.SUPPORTED
    scalar = next(item for item in report.hypotheses if item.id == SCALAR_THRESHOLD_HYPOTHESIS.id)
    assert scalar.status is HypothesisStatus.REFUTED
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    wide = plan_signed_digit_pair(3, 1, remaining=4)
    closure = next(item for item in wide.results if item.name == "closure")
    assert closure.status is AttackStatus.SUPPORTED
    assert closure.evidence.get("union_size") == 1


def test_export_links_lean_and_records_write(tmp_path):
    report = plan_signed_digit_residual(4)
    targets = export_signed_digit_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "signed_digit_residual"
    assert (RECORD_DIR / "closure.yaml").is_file()
    assert (RECORD_DIR / "family.yaml").is_file()
