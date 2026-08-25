"""Signed-digit residual geometry inside the finite envelope."""

from __future__ import annotations

from research.open_problems import get_problem
from research.signed_digit_residual_geometry.discovery import (
    PROBES,
    geometry_report,
    lambda1_climb,
    lambda2_even_climb,
    predicted_symmetric,
    probe_report,
    sign_symmetry_halves_mealy,
    singleton_two_witness,
)
from research.signed_digit_residual_geometry.lean_export import (
    CLOSURE_THEOREM,
    export_geometry_targets,
    closure_is_exact_size,
)
from research.signed_digit_residual_geometry.planner import (
    CLOSURE_HYPOTHESIS,
    LATTICE_ALL_U_HYPOTHESIS,
    SIGN_MEALY_HYPOTHESIS,
    plan_signed_digit_residual_geometry,
)
from research.signed_digit_residual_geometry.problem import PROBLEM
from research.signed_digit_residual_geometry.records import RECORD_DIR, write_records
from research.signed_digit_residual_geometry.spec import geometry_spec
from research.signed_digit_residual.spec import SignedDigitResidualSpec
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_problem_is_registered():
    assert get_problem("signed_digit_residual_geometry") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/signed_digit_residual_geometry.md",)


def test_lambda1_interval_is_full_and_climbs():
    for bound in range(0, 7):
        report = geometry_report(1, bound)
        predicted = predicted_symmetric(1, bound)
        assert report["matches_lattice_box"] is True
        assert report["reachable"] == predicted
        assert report["mealy"] == report["reachable_count"]
        radius = bound // 2
        for target in range(-radius, radius + 1):
            assert lambda1_climb(target) == target


def test_lambda2_evens_fill_the_sharp_box():
    for bound in range(0, 7):
        report = geometry_report(2, bound)
        assert report["matches_lattice_box"] is True
        assert report["mealy"] == report["reachable_count"]
        assert report["reachable"] == predicted_symmetric(2, bound)
        half = max(bound - 1, 0)
        for step in range(-half, half + 1):
            assert lambda2_even_climb(step) == 2 * step


def test_critical_lambda3_m1_is_origin():
    report = geometry_report(3, 1)
    assert report["reachable"] == (0,)
    assert report["mealy"] == 1
    assert report["matches_lattice_box"] is True


def test_lattice_box_fails_on_one_sided_alphabets():
    witness = singleton_two_witness()
    assert witness["reachable"] == (0, 1)
    assert witness["missing"] == (-1,)
    assert witness["matches_lattice_box"] is False
    assert witness["mealy"] == 2
    for alphabet in PROBES:
        one = probe_report(alphabet, 1)
        two = probe_report(alphabet, 2)
        assert one["mealy"] == one["reachable_count"]
        assert two["mealy"] == two["reachable_count"]
    sparse = probe_report((-2, 0, 2), 1)
    assert sparse["matches_lattice_box"] is True
    asymmetric = probe_report((0, 1, 2), 1)
    assert asymmetric["reachable"] == (0, 1)
    assert asymmetric["missing"] == (-1,)


def test_sign_symmetry_does_not_halve_mealy():
    assert sign_symmetry_halves_mealy(1, 2) is False
    assert sign_symmetry_halves_mealy(2, 2) is False


def test_spec_reuses_signed_digit_and_planner():
    spec = geometry_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert isinstance(spec, SignedDigitResidualSpec)
    assert spec.name == "signed_digit_residual_geometry"
    assert spec.affine_system() is None
    report = plan_signed_digit_residual_geometry(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 3)
    hyp = next(item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id)
    assert hyp.status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == LATTICE_ALL_U_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == SIGN_MEALY_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED


def test_export_links_lean_and_records(tmp_path):
    report = plan_signed_digit_residual_geometry(4)
    targets = export_geometry_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "signed_digit_residual_geometry"
    write_records(report, targets)
    assert (RECORD_DIR / "closure.yaml").is_file()
