"""Signed-digit residual rigidity under constrained controls."""

from __future__ import annotations

from research.open_problems import get_problem
from research.signed_digit_constrained_controls.discovery import (
    any_word_separates,
    bisimilar_parity_collapses_controls,
    constant_word_is_required,
    model_family,
    norepeat_u2_product_size,
    parity_automaton,
    residual_merge_exists,
)
from research.signed_digit_constrained_controls.lean_export import (
    CLOSURE_THEOREM,
    closure_is_exact_size,
    export_constrained_targets,
)
from research.signed_digit_constrained_controls.planner import (
    CLOSURE_HYPOTHESIS,
    CONSTANT_HYPOTHESIS,
    MERGE_HYPOTHESIS,
    plan_signed_digit_constrained_controls,
)
from research.signed_digit_constrained_controls.problem import PROBLEM
from research.signed_digit_constrained_controls.records import RECORD_DIR, write_records
from research.signed_digit_constrained_controls.spec import ConstrainedNoRepeatSpec, constrained_spec
from research.signed_digit_residual.discovery import alphabet_m
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_problem_is_registered():
    assert get_problem("signed_digit_constrained_controls") is PROBLEM
    assert PROBLEM.status == "STRUCTURAL"
    assert PROBLEM.docs == ("docs/problems/signed_digit_constrained_controls.md",)


def test_any_word_of_critical_length_separates():
    assert any_word_separates(0, 3, (0, 0), 1) is True
    assert any_word_separates(0, 3, (1, 2), 1) is True
    assert any_word_separates(0, 3, (2, 1), 1) is True
    assert any_word_separates(0, 3, (0,), 1) is False
    assert any_word_separates(0, 6, (0, 0), 2) is True


def test_models_have_no_residual_merge():
    assert residual_merge_exists() is False
    assert constant_word_is_required() is False
    assert norepeat_u2_product_size(1) == 10
    for gain in (1, 2):
        reports = model_family(gain)
        names = [item["name"] for item in reports]
        assert names == [
            "A_periodic",
            "B_alternating",
            "C_norepeat",
            "D_parity",
            "D_parity",
        ]
        for item in reports:
            assert item["residual_merges"] == ()
        norep = reports[2]
        assert norep["minimal_product"] is True


def test_no_repeat_forbids_constants_but_stays_minimal():
    report = next(item for item in model_family(1) if item["name"] == "C_norepeat")
    assert report["product_count"] == 10
    assert report["mealy"] == 10
    assert report["minimal_product"] is True


def test_bisimilar_parity_collapses_control_not_residual():
    assert bisimilar_parity_collapses_controls() is True
    report = constrained_parity_equal()
    assert report["mealy"] == report["residual_count"]
    assert report["mealy"] < report["product_count"]
    assert report["residual_merges"] == ()


def constrained_parity_equal():
    from research.signed_digit_constrained_controls.discovery import constrained_report

    return constrained_report(parity_automaton(alphabet_m(2), alphabet_m(2)), 1)


def test_spec_is_product_and_planner():
    spec = constrained_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert isinstance(spec, ConstrainedNoRepeatSpec)
    assert spec.name == "signed_digit_constrained_controls"
    assert spec.affine_system() is None
    assert spec.dimension == 2
    report = plan_signed_digit_constrained_controls(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_size(report, 10)
    hyp = next(item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id)
    assert hyp.status is HypothesisStatus.SUPPORTED
    assert next(
        item for item in report.hypotheses if item.id == CONSTANT_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED
    assert next(
        item for item in report.hypotheses if item.id == MERGE_HYPOTHESIS.id
    ).status is HypothesisStatus.REFUTED


def test_export_links_lean_and_records(tmp_path):
    report = plan_signed_digit_constrained_controls(4)
    targets = export_constrained_targets(report)
    closure = next(item for item in targets if item.attack == "closure")
    assert closure.exportable
    assert closure.lean_theorem == CLOSURE_THEOREM
    assert all(not (item.kind is ClaimKind.LIVE and item.exportable) for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    assert RECORD_DIR.name == "signed_digit_constrained_controls"
    write_records(report, targets)
    assert (RECORD_DIR / "closure.yaml").is_file()
