"""v2 control of T(n)=W(n). Does not reopen digit-sum or SignedP0."""

from __future__ import annotations

from research.balanced_ternary_digit_sum_dynamics.problem import (
    PROBLEM as DIGIT_SUM,
)
from research.balanced_ternary_weight_dynamics.discovery import (
    distinct_orbits_witness,
    envelope_versus_orbit,
    even_map_counterexample,
    idempotent_counterexample,
    interval_leak_witness,
    lyapunov_n_witness,
    magnitude_drop_counterexample,
    matches_certified_weight,
    matches_oeis_prefix,
    max_orbit_size,
    odd_map_counterexample,
    orbit_of,
    seed_complexity_profile,
)
from research.balanced_ternary_weight_dynamics.lean_export import (
    CLOSURE_THEOREM,
    closure_is_exact_size,
    export_weight_targets,
)
from research.balanced_ternary_weight_dynamics.planner import (
    CLOSURE_HYPOTHESIS,
    CONTRACTION_GE2_HYPOTHESIS,
    CONTRACTION_GE3_HYPOTHESIS,
    EVEN_HYPOTHESIS,
    GLOBAL_RESIDUAL_HYPOTHESIS,
    IDENTITY_MERGE_HYPOTHESIS,
    IDEMPOTENT_HYPOTHESIS,
    INTERVAL_HYPOTHESIS,
    LYAPUNOV_HYPOTHESIS,
    plan_weight_dynamics,
)
from research.balanced_ternary_weight_dynamics.problem import PROBLEM
from research.balanced_ternary_weight_dynamics.records import RECORD_DIR, write_records
from research.balanced_ternary_weight_dynamics.spec import (
    WeightDynamicsSpec,
    digit_square_sum,
    weight_dynamics_spec,
)
from research.literature import get_reference
from research.open_problems import get_problem
from research.operator_dynamics.signed_p0.problem import PROBLEM as SIGNED_P0
from research_engine.attacks.result import AttackStatus
from research_engine.attacks.separation import separate_states
from research_engine.core.observation import observe
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind
from research_engine.planner.hypothesis import HypothesisStatus


def test_prior_art_a005812_is_registered():
    rec = get_reference("oeis-A005812")
    assert rec["identifiers"]["oeis"] == "A005812"
    assert rec["project_relationship"] == "known"


def test_closed_digit_fold_branches_stay_registered():
    assert get_problem("balanced_ternary_digit_sum_dynamics") is DIGIT_SUM
    assert get_problem("operator_dynamics_benchmark") is SIGNED_P0


def test_benchmark_problem_is_registered():
    assert get_problem("balanced_ternary_weight_dynamics") is PROBLEM
    assert PROBLEM.status == "ARCHIVED"
    assert PROBLEM.docs == ("docs/problems/balanced_ternary_weight_dynamics.md",)


def test_local_semantics_match_certified_weight():
    assert matches_certified_weight() is True
    assert matches_oeis_prefix() is True
    assert digit_square_sum(0) == 0
    assert digit_square_sum(1) == 1
    assert digit_square_sum(2) == 2
    assert digit_square_sum(-2) == 2
    assert digit_square_sum(4) == 2
    assert digit_square_sum(5) == 3


def test_orbit_and_falsifiers():
    assert magnitude_drop_counterexample(min_abs=2) is not None
    assert abs(magnitude_drop_counterexample(min_abs=2)) == 2
    assert magnitude_drop_counterexample(min_abs=3) is None
    assert even_map_counterexample() is None
    assert odd_map_counterexample() is not None
    counter = idempotent_counterexample()
    assert counter is not None
    assert digit_square_sum(digit_square_sum(counter)) != digit_square_sum(counter)
    assert orbit_of(4) == (4, 2)
    assert orbit_of(5) == (5, 3, 1)
    left, right = distinct_orbits_witness()
    assert set(orbit_of(left)).isdisjoint(orbit_of(right))
    assert max_orbit_size() >= 2


def test_refutations_and_envelope():
    assert interval_leak_witness() is None
    assert lyapunov_n_witness() == 0
    comparison = envelope_versus_orbit(4)
    assert comparison.envelope_equals_reachable is False
    assert (4,) in comparison.extra
    assert (0,) in comparison.holes


def test_identity_observation():
    spec = weight_dynamics_spec(4)
    phase = spec.initial_phase()
    assert observe(spec, (4,), 0, phase) == 4
    assert spec.output((4,), 0, phase) == 4
    assert spec.affine_system() is None


def test_spec_and_planner():
    spec = weight_dynamics_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert isinstance(spec, WeightDynamicsSpec)
    assert spec.name == "balanced_ternary_weight_dynamics"
    report = plan_weight_dynamics(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.certificate_kind is CertificateKind.BOUNDED_RECONNAISSANCE
    assert closure_is_exact_size(report, 2)
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
    assert quotient.evidence.get("reachable_state_count") == 2
    assert quotient.evidence.get("quotient_count") == 2
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
        item for item in report.hypotheses if item.id == CONTRACTION_GE2_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == CONTRACTION_GE3_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == EVEN_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED


def test_separation_and_profile():
    spec = weight_dynamics_spec(4)
    split = separate_states(spec, (4,), (2,))
    assert split.separated is True
    profile = seed_complexity_profile()
    assert profile.control_count == 1
    assert profile.reachable_state_count == 2
    assert profile.behavioral_state_count == 2
    assert profile.minimal_machine_count == 2
    assert profile.closure_status == "EXACT_CLOSURE"
    assert profile.raw_contribution_count is None


def test_export_links_lean_and_records(tmp_path):
    report = plan_weight_dynamics(4)
    targets = export_weight_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "weight_dynamics"
    write_records(report, targets)
    assert (RECORD_DIR / "closure.yaml").is_file()
