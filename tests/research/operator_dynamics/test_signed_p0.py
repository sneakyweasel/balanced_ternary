"""v2 benchmark of N∘I₀∘D. Does not reopen the {S,N,D,W} census."""

from __future__ import annotations

from research.open_problems import get_problem
from research.operator_dynamics.problem import PROBLEM as ARCHIVED
from research.operator_dynamics.signed_p0.discovery import (
    distinct_orbits_witness,
    envelope_versus_orbit,
    f2_equals_p0,
    f2_p0_counterexample,
    fab_is_section_on_probes,
    interval_leak_witness,
    lsd_after_one_step_is_zero,
    lyapunov_n_witness,
    max_orbit_size,
    orbit_of,
    seed_complexity_profile,
    sign_stream,
)
from research.operator_dynamics.signed_p0.lean_export import (
    CLOSURE_THEOREM,
    closure_is_exact_size,
    export_signed_p0_targets,
)
from research.operator_dynamics.signed_p0.planner import (
    CLOSURE_HYPOTHESIS,
    F2_HYPOTHESIS,
    GLOBAL_RESIDUAL_HYPOTHESIS,
    INTERVAL_HYPOTHESIS,
    LYAPUNOV_HYPOTHESIS,
    SIGN_MERGE_HYPOTHESIS,
    plan_signed_p0,
)
from research.operator_dynamics.signed_p0.problem import PROBLEM
from research.operator_dynamics.signed_p0.records import RECORD_DIR, write_records
from research.operator_dynamics.signed_p0.spec import (
    SignedP0Spec,
    integer_sign,
    p0,
    predecessors,
    signed_p0,
    signed_p0_spec,
)
from research_engine.attacks.result import AttackStatus
from research_engine.attacks.separation import separate_states
from research_engine.core.observation import observe
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_archived_census_stays_registered():
    assert ARCHIVED.status == "ARCHIVED"
    assert get_problem("operator_dynamics") is ARCHIVED


def test_benchmark_problem_is_registered():
    assert get_problem("operator_dynamics_benchmark") is PROBLEM
    assert PROBLEM.status == "ARCHIVED"
    assert PROBLEM.docs == ("docs/problems/operator_dynamics_benchmark.md",)


def test_fab_collapses_and_nsd_does_not():
    assert fab_is_section_on_probes() is True
    assert signed_p0(5) == -p0(5)
    assert signed_p0(5) != 5
    assert signed_p0(5) != -5
    assert signed_p0(5) != 3 * 5
    assert signed_p0(5) != signed_p0(signed_p0(5)) or 5 != 0


def test_orbit_law_on_probes():
    assert f2_p0_counterexample() is None
    assert lsd_after_one_step_is_zero() is True
    for n in range(-20, 21):
        assert f2_equals_p0(n)
        assert signed_p0(signed_p0(signed_p0(n))) == signed_p0(n)
        assert len(orbit_of(n)) <= 3
    assert orbit_of(4) == (4, -3, 3)
    assert max_orbit_size() <= 3
    left, right = distinct_orbits_witness()
    assert set(orbit_of(left)).isdisjoint(orbit_of(right))


def test_refutations_and_envelope():
    src, image = interval_leak_witness()
    assert abs(src) <= 2
    assert abs(image) > 2
    assert signed_p0(2) == -3
    assert lyapunov_n_witness() is not None
    comparison = envelope_versus_orbit(4)
    assert comparison.envelope_equals_reachable is False
    assert (4,) in comparison.extra
    assert (0,) in comparison.holes


def test_sign_observation_and_preimages():
    spec = signed_p0_spec(4)
    phase = spec.initial_phase()
    assert observe(spec, (4,), 0, phase) == integer_sign(4) == 1
    assert spec.output((4,), 0, phase) == 1
    assert spec.affine_system() is None
    assert not hasattr(spec, "raw_contribution") or not callable(
        getattr(spec, "raw_contribution", None)
    )
    assert predecessors(0) == (-1, 0, 1)
    assert predecessors(1) == ()
    assert sign_stream(4, 4) == (1, -1, 1, -1)


def test_spec_and_planner():
    spec = signed_p0_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert isinstance(spec, SignedP0Spec)
    assert spec.name == "operator_dynamics_benchmark"
    assert spec.dimension == 1
    report = plan_signed_p0(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.certificate_kind is CertificateKind.BOUNDED_RECONNAISSANCE
    assert closure_is_exact_size(report, 3)
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    assert "factorization" in skipped
    assert "block" in skipped
    assert "symbolic" in skipped
    affine = next(item for item in report.results if item.name == "affine")
    assert affine.status is AttackStatus.REFUTED
    assert affine.certificate_kind is CertificateKind.EXACT_COUNTEREXAMPLE
    quotient = next(item for item in report.results if item.name == "quotient")
    assert quotient.status is AttackStatus.SUPPORTED
    assert quotient.evidence.get("reachable_state_count") == 3
    assert quotient.evidence.get("quotient_count") == 2
    assert next(
        item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == INTERVAL_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == LYAPUNOV_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == GLOBAL_RESIDUAL_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == F2_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == SIGN_MERGE_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED


def test_separation_and_profile():
    spec = signed_p0_spec(4)
    split = separate_states(spec, (4,), (-3,))
    assert split.separated is True
    assert split.certificate_kind is CertificateKind.EXACT_COUNTEREXAMPLE
    merged = separate_states(spec, (4,), (3,))
    assert merged.separated is False
    assert merged.scope is SearchScope.EXACT
    profile = seed_complexity_profile()
    assert profile.control_count == 1
    assert profile.reachable_state_count == 3
    assert profile.behavioral_state_count == 2
    assert profile.minimal_machine_count == 2
    assert profile.closure_status == "EXACT_CLOSURE"
    assert profile.raw_contribution_count is None


def test_export_links_lean_and_records(tmp_path):
    report = plan_signed_p0(4)
    targets = export_signed_p0_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "operator_dynamics"
    write_records(report, targets)
    assert (RECORD_DIR / "closure.yaml").is_file()
