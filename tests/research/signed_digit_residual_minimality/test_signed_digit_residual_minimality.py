"""Signed-digit residual behavioral minimality."""

from __future__ import annotations

from research.open_problems import get_problem
from research.signed_digit_residual.discovery import alphabet_m
from research.signed_digit_residual_minimality.discovery import (
    SEARCH_ALPHABETS,
    first_merge,
    lambda1_zero_three_witness,
    lambda3_translate_witness,
    minimality_report,
    mod3_does_not_merge,
    predicted_sep_len,
    search_is_minimal,
    search_reports,
    shortest_separating_word,
    symmetric_family_minimal,
    val3,
)
from research.signed_digit_residual_minimality.lean_export import (
    CLOSURE_THEOREM,
    closure_is_exact_size,
    export_minimality_targets,
)
from research.signed_digit_residual_minimality.planner import (
    CLOSURE_HYPOTHESIS,
    MERGE_HYPOTHESIS,
    MOD3_HYPOTHESIS,
    plan_signed_digit_residual_minimality,
)
from research.signed_digit_residual_minimality.problem import PROBLEM
from research.signed_digit_residual_minimality.records import RECORD_DIR, write_records
from research.signed_digit_residual_minimality.spec import minimality_spec
from research.signed_digit_residual.spec import SignedDigitResidualSpec
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_problem_is_registered():
    assert get_problem("signed_digit_residual_minimality") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/signed_digit_residual_minimality.md",)


def test_search_alphabets_are_minimal():
    assert SEARCH_ALPHABETS[0] == (0, 1)
    assert first_merge() is None
    assert search_is_minimal() is True
    for gain in (1, 2):
        for report in search_reports(gain):
            assert report["minimal"] is True
            assert report["mealy"] == report["reachable_count"]
            assert report["merged"] == ()


def test_val3_predicts_separating_length():
    assert val3(1) == 0
    assert val3(3) == 1
    assert val3(9) == 2
    assert val3(18) == 2
    assert predicted_sep_len(0, 3) == 2
    assert predicted_sep_len(0, 9) == 3
    word = shortest_separating_word(0, 3, (0,), 1)
    assert word == (0, 0)
    assert shortest_separating_word(0, 6, (0,), 2) == (0, 0)


def test_mod3_same_signature_is_not_a_merge():
    witness = lambda1_zero_three_witness()
    assert witness["same_immediate_signature"] is True
    assert witness["word"] == (0, 0)
    assert witness["matches_val3"] is True
    assert mod3_does_not_merge() is True
    assert lambda3_translate_witness()["word"] is None


def test_symmetric_family_matches_val3_and_is_minimal():
    assert symmetric_family_minimal(6) is True
    report = minimality_report(alphabet_m(6), 1)
    assert report["reachable"] == tuple(range(-3, 4))
    assert report["mealy"] == 7
    assert report["L_max"] == 2
    lambda2 = minimality_report(alphabet_m(6), 2)
    assert lambda2["mealy"] == lambda2["reachable_count"]
    assert lambda2["L_max"] == 3


def test_spec_reuses_signed_digit_and_planner():
    spec = minimality_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert isinstance(spec, SignedDigitResidualSpec)
    assert spec.name == "signed_digit_residual_minimality"
    assert spec.affine_system() is None
    report = plan_signed_digit_residual_minimality(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 3)
    hyp = next(item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id)
    assert hyp.status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == MERGE_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == MOD3_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED


def test_export_links_lean_and_records(tmp_path):
    report = plan_signed_digit_residual_minimality(4)
    targets = export_minimality_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "signed_digit_residual_minimality"
    write_records(report, targets)
    assert (RECORD_DIR / "closure.yaml").is_file()
