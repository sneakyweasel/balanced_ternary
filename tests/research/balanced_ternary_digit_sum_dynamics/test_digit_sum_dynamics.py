"""v2 benchmark of T(n)=s(n). Does not reopen polynomial digit-sum level sets."""

from __future__ import annotations

from research.balanced_digit_sum_polynomials.problem import (
    PROBLEM as POLYNOMIAL_DIGIT_SUM,
)
from research.balanced_ternary_digit_sum_dynamics.discovery import (
    distinct_orbits_witness,
    envelope_versus_orbit,
    idempotent_counterexample,
    interval_leak_witness,
    lyapunov_n_witness,
    magnitude_drop_counterexample,
    matches_certified_digit_sum,
    matches_oeis_prefix,
    max_orbit_size,
    odd_map_counterexample,
    orbit_of,
    seed_complexity_profile,
)
from research.balanced_ternary_digit_sum_dynamics.lean_export import (
    CLOSURE_THEOREM,
    closure_is_exact_size,
    export_digit_sum_targets,
)
from research.balanced_ternary_digit_sum_dynamics.planner import (
    CLOSURE_HYPOTHESIS,
    CONTRACTION_HYPOTHESIS,
    GLOBAL_RESIDUAL_HYPOTHESIS,
    IDENTITY_MERGE_HYPOTHESIS,
    IDEMPOTENT_HYPOTHESIS,
    INTERVAL_HYPOTHESIS,
    LYAPUNOV_HYPOTHESIS,
    plan_digit_sum_dynamics,
)
from research.balanced_ternary_digit_sum_dynamics.problem import PROBLEM
from research.balanced_ternary_digit_sum_dynamics.records import RECORD_DIR, write_records
from research.balanced_ternary_digit_sum_dynamics.spec import (
    DigitSumDynamicsSpec,
    digit_sum,
    digit_sum_spec,
)
from research.open_problems import get_problem
from research_engine.attacks.result import AttackStatus
from research_engine.attacks.separation import separate_states
from research_engine.core.observation import observe
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind
from research_engine.planner.hypothesis import HypothesisStatus


def test_polynomial_digit_sum_stays_closed():
    assert POLYNOMIAL_DIGIT_SUM.id == "balanced_digit_sum_polynomials"
    assert get_problem("balanced_digit_sum_polynomials") is POLYNOMIAL_DIGIT_SUM


def test_benchmark_problem_is_registered():
    assert get_problem("balanced_ternary_digit_sum_dynamics") is PROBLEM
    assert PROBLEM.status == "ARCHIVED"
    assert PROBLEM.docs == ("docs/problems/balanced_ternary_digit_sum_dynamics.md",)


def test_local_semantics_match_certified_sum():
    assert matches_certified_digit_sum() is True
    assert matches_oeis_prefix() is True
    assert digit_sum(0) == 0
    assert digit_sum(1) == 1
    assert digit_sum(2) == 0
    assert digit_sum(4) == 2
    assert digit_sum(5) == -1


def test_orbit_and_falsifiers():
    assert magnitude_drop_counterexample() is None
    counter = idempotent_counterexample()
    assert counter is not None
    assert digit_sum(digit_sum(counter)) != digit_sum(counter)
    assert digit_sum(digit_sum(4)) != digit_sum(4)
    assert odd_map_counterexample() is None
    assert orbit_of(4) == (4, 2, 0)
    assert orbit_of(5) == (5, -1)
    left, right = distinct_orbits_witness()
    assert set(orbit_of(left)).isdisjoint(orbit_of(right))
    assert max_orbit_size() >= 2


def test_refutations_and_envelope():
    assert interval_leak_witness() is None
    assert lyapunov_n_witness() == 0
    comparison = envelope_versus_orbit(4)
    assert comparison.envelope_equals_reachable is False
    assert (4,) in comparison.extra
    assert (1,) in comparison.holes


def test_identity_observation():
    spec = digit_sum_spec(4)
    phase = spec.initial_phase()
    assert observe(spec, (4,), 0, phase) == 4
    assert spec.output((4,), 0, phase) == 4
    assert spec.affine_system() is None
    assert not hasattr(spec, "raw_contribution") or not callable(
        getattr(spec, "raw_contribution", None)
    )


def test_spec_and_planner():
    spec = digit_sum_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert isinstance(spec, DigitSumDynamicsSpec)
    assert spec.name == "balanced_ternary_digit_sum_dynamics"
    assert spec.dimension == 1
    report = plan_digit_sum_dynamics(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.certificate_kind is CertificateKind.BOUNDED_RECONNAISSANCE
    assert closure_is_exact_size(report, 3)
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    assert "factorization" in skipped
    assert "block" in skipped
    assert "reverse" in skipped
    assert "symmetry" in skipped
    assert "symbolic" in skipped
    affine = next(item for item in report.results if item.name == "affine")
    assert affine.status is AttackStatus.OBSERVATION
    quotient = next(item for item in report.results if item.name == "quotient")
    assert quotient.status is AttackStatus.SUPPORTED
    assert quotient.evidence.get("reachable_state_count") == 3
    assert quotient.evidence.get("quotient_count") == 3
    assert next(
        item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == INTERVAL_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == LYAPUNOV_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == GLOBAL_RESIDUAL_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == IDENTITY_MERGE_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == IDEMPOTENT_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == CONTRACTION_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED


def test_separation_and_profile():
    spec = digit_sum_spec(4)
    split = separate_states(spec, (4,), (2,))
    assert split.separated is True
    profile = seed_complexity_profile()
    assert profile.control_count == 1
    assert profile.reachable_state_count == 3
    assert profile.behavioral_state_count == 3
    assert profile.minimal_machine_count == 3
    assert profile.closure_status == "EXACT_CLOSURE"
    assert profile.raw_contribution_count is None


def test_export_links_lean_and_records(tmp_path):
    report = plan_digit_sum_dynamics(4)
    targets = export_digit_sum_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "digit_sum_dynamics"
    write_records(report, targets)
    assert (RECORD_DIR / "closure.yaml").is_file()
