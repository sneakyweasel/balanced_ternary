"""v2 benchmark of T(n)=n+W(n). Does not reopen digit-fold branches."""

from __future__ import annotations

from research.balanced_ternary_digit_sum_dynamics.problem import (
    PROBLEM as DIGIT_SUM,
)
from research.balanced_ternary_weight_dynamics.problem import (
    PROBLEM as WEIGHT,
)
from research.balanced_ternary_weight_drift.discovery import (
    even_map_counterexample,
    idempotent_counterexample,
    interval_leak_witness,
    lyapunov_n_witness,
    magnitude_drop_counterexample,
    matches_certified_weight,
    nonpos_invariant_counterexample,
    orbit_intersection_witness,
    orbit_of,
    seed_complexity_profile,
    strict_increase_counterexample,
)
from research.balanced_ternary_weight_drift.lean_export import (
    DRIFT_THEOREM,
    closure_is_inconclusive,
    export_weight_drift_targets,
)
from research.balanced_ternary_weight_drift.planner import (
    CLOSURE_HYPOTHESIS,
    CONTRACTION_HYPOTHESIS,
    DISJOINT_HYPOTHESIS,
    EVEN_HYPOTHESIS,
    GLOBAL_RESIDUAL_HYPOTHESIS,
    IDENTITY_MERGE_HYPOTHESIS,
    IDEMPOTENT_HYPOTHESIS,
    INCREASE_HYPOTHESIS,
    INTERVAL_HYPOTHESIS,
    LYAPUNOV_HYPOTHESIS,
    NONPOS_HYPOTHESIS,
    plan_weight_drift,
)
from research.balanced_ternary_weight_drift.problem import PROBLEM
from research.balanced_ternary_weight_drift.records import RECORD_DIR, write_records
from research.balanced_ternary_weight_drift.spec import (
    WeightDriftSpec,
    weight_drift,
    weight_drift_spec,
)
from research.literature import get_reference
from research.open_problems import get_problem
from research.operator_dynamics.signed_p0.problem import PROBLEM as SIGNED_P0
from research_engine.attacks.result import AttackStatus
from research_engine.attacks.separation import separate_states
from research_engine.core.observation import observe
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind
from research_engine.planner.hypothesis import HypothesisStatus


def test_prior_art_kaprekar_generator_is_registered():
    rec = get_reference("oeis-A062028")
    assert rec["identifiers"]["oeis"] == "A062028"
    assert rec["project_relationship"] == "known"


def test_closed_digit_fold_branches_stay_registered():
    assert get_problem("balanced_ternary_digit_sum_dynamics") is DIGIT_SUM
    assert get_problem("balanced_ternary_weight_dynamics") is WEIGHT
    assert get_problem("operator_dynamics_benchmark") is SIGNED_P0


def test_benchmark_problem_is_registered():
    assert get_problem("balanced_ternary_weight_drift") is PROBLEM
    assert PROBLEM.status == "ARCHIVED"
    assert PROBLEM.docs == ("docs/problems/balanced_ternary_weight_drift.md",)


def test_local_semantics_are_n_plus_weight():
    assert matches_certified_weight() is True
    assert weight_drift(0) == 0
    assert weight_drift(1) == 2
    assert weight_drift(2) == 4
    assert weight_drift(-1) == 0
    assert weight_drift(-2) == 0
    assert weight_drift(4) == 6
    assert weight_drift(5) == 8


def test_orbit_and_falsifiers():
    assert magnitude_drop_counterexample(min_abs=2) is not None
    assert magnitude_drop_counterexample(min_abs=2) == 2
    assert even_map_counterexample() is not None
    assert strict_increase_counterexample() is None
    assert nonpos_invariant_counterexample() is None
    counter = idempotent_counterexample()
    assert counter is not None
    assert weight_drift(weight_drift(counter)) != weight_drift(counter)
    assert orbit_of(4)[:3] == (4, 6, 8)
    assert orbit_of(-4) == (-4, -2, 0)
    left, right, meet = orbit_intersection_witness()
    assert left == 4 and right == 5
    assert meet == 8


def test_refutations_and_envelope():
    leak = interval_leak_witness()
    assert leak == (2, 4)
    assert lyapunov_n_witness() == 0


def test_identity_observation():
    spec = weight_drift_spec(4)
    phase = spec.initial_phase()
    assert observe(spec, (4,), 0, phase) == 4
    assert spec.output((4,), 0, phase) == 4
    assert spec.affine_system() is None


def test_spec_and_planner():
    spec = weight_drift_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert isinstance(spec, WeightDriftSpec)
    assert spec.name == "balanced_ternary_weight_drift"
    report = plan_weight_drift(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert closure_is_inconclusive(report) is True
    functional = next(item for item in report.results if item.name == "functional")
    assert functional.status is AttackStatus.REFUTED
    affine = next(item for item in report.results if item.name == "affine")
    assert affine.status is AttackStatus.REFUTED
    quotient = next(item for item in report.results if item.name == "quotient")
    assert quotient.status is AttackStatus.INCONCLUSIVE
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    assert "factorization" in skipped
    assert "block" in skipped
    assert "reverse" in skipped
    assert "symmetry" in skipped
    assert "symbolic" in skipped
    statuses = {item.id: item.status for item in report.hypotheses}
    assert statuses[CLOSURE_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[INTERVAL_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[LYAPUNOV_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[GLOBAL_RESIDUAL_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[IDENTITY_MERGE_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[IDEMPOTENT_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[CONTRACTION_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[EVEN_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[DISJOINT_HYPOTHESIS.id] is HypothesisStatus.REFUTED
    assert statuses[INCREASE_HYPOTHESIS.id] is HypothesisStatus.SUPPORTED
    assert statuses[NONPOS_HYPOTHESIS.id] is HypothesisStatus.SUPPORTED


def test_separation_and_profile():
    spec = weight_drift_spec(4)
    split = separate_states(spec, (4,), (6,))
    assert split.separated is True
    profile = seed_complexity_profile()
    assert profile.control_count == 1
    assert profile.reachable_state_count == spec.state_cap + 1
    assert profile.closure_status == "INCONCLUSIVE"
    assert profile.raw_contribution_count is None


def test_export_links_lean_and_records(tmp_path):
    report = plan_weight_drift(4)
    targets = export_weight_drift_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable is False
    drift = next(item for item in targets if item.lean_theorem == DRIFT_THEOREM)
    assert drift.exportable
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "weight_drift"
    write_records(report, targets)
    assert (RECORD_DIR / "closure.yaml").is_file()
