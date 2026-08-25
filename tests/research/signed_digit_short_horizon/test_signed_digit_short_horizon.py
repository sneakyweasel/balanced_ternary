"""Finite-horizon control versus 3-adic residual separation."""

from __future__ import annotations

from research.open_problems import get_problem
from research.signed_digit_residual.discovery import alphabet_m
from research.signed_digit_short_horizon.discovery import (
    asymmetric_obeys_local_truncation,
    coprime_sweep,
    genuine_merge_exists,
    horizon_u2_product_size,
    lambda3_deadlock_merges_everything,
    lambda3_positive_horizon_is_translation,
    only_deadlock_merges,
    origin_reachable_positive_horizon_residual_merge,
    pair_report,
    shorter_always_separates,
    smallest_genuine_merge,
    truncated_congruence_holds,
)
from research.signed_digit_short_horizon.lean_export import (
    CLOSURE_THEOREM,
    closure_is_exact_size,
    export_short_horizon_targets,
)
from research.signed_digit_short_horizon.planner import (
    CLOSURE_HYPOTHESIS,
    DEADLOCK_HYPOTHESIS,
    MERGE_HYPOTHESIS,
    SHORT_SEP_HYPOTHESIS,
    plan_signed_digit_short_horizon,
)
from research.signed_digit_short_horizon.problem import PROBLEM
from research.signed_digit_short_horizon.records import RECORD_DIR, write_records
from research.signed_digit_short_horizon.spec import ShortHorizonSpec, short_horizon_spec
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_problem_is_registered():
    assert get_problem("signed_digit_short_horizon") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/signed_digit_short_horizon.md",)


def test_truncated_congruence_on_listed_pairs():
    assert truncated_congruence_holds(1) is True
    assert truncated_congruence_holds(2) is True
    assert genuine_merge_exists() is True
    assert smallest_genuine_merge() == (0, 3, 1)
    row = pair_report(0, 3, 1)
    assert row["agree"] is True
    assert row["genuine_merge"] is True
    assert row["deadlock"] is False
    assert pair_report(0, 3, 0)["deadlock"] is True
    assert pair_report(0, 3, 2)["agree"] is False
    assert pair_report(0, 9, 2)["agree"] is True
    assert pair_report(0, 9, 3)["agree"] is False
    assert pair_report(0, 27, 3)["agree"] is True
    assert pair_report(0, 27, 4)["agree"] is False


def test_h2_and_h3_are_false():
    assert shorter_always_separates() is False
    assert only_deadlock_merges() is False
    assert origin_reachable_positive_horizon_residual_merge() is False
    assert horizon_u2_product_size(1) == 7
    assert asymmetric_obeys_local_truncation() is True


def test_lambda3_adds_no_positive_horizon_classes():
    assert lambda3_positive_horizon_is_translation() is True
    assert lambda3_deadlock_merges_everything() is True


def test_sweep_matches_mod_pow():
    for row in coprime_sweep(1, alphabet_m(1)):
        assert row["agree"] is row["predicted_mod"]


def test_spec_is_product_and_planner():
    spec = short_horizon_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert isinstance(spec, ShortHorizonSpec)
    assert spec.name == "signed_digit_short_horizon"
    assert spec.affine_system() is None
    assert spec.dimension == 2
    assert len(spec.candidate_region) == 7
    report = plan_signed_digit_short_horizon(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 7)
    assert next(
        item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == MERGE_HYPOTHESIS.id
    ).status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == SHORT_SEP_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == DEADLOCK_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED


def test_export_links_lean_and_records(tmp_path):
    report = plan_signed_digit_short_horizon(4)
    targets = export_short_horizon_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "signed_digit_short_horizon"
    write_records(report, targets)
    assert (RECORD_DIR / "closure.yaml").is_file()
