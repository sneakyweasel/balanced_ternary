"""First real-problem campaign: unmodified ResearchLoop on A–D."""

from __future__ import annotations

from pathlib import Path

from research.engine_campaign.candidates import spec_for_selection
from research.engine_campaign.corpus import seed_baseline_corpus
from research.engine_campaign.problem import PROBLEM
from research.engine_campaign.runner import FAMILY_PAIRS, run_campaign
from research.open_problems import get_problem
from research_engine.diagnosis.compare import core_match
from research_engine.diagnosis.family import family_status_for
from research_engine.diagnosis.types import FamilyStatus, ResearchDecision


def test_problem_descriptor_and_no_collatz_import():
    assert get_problem("engine_campaign") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/engine_campaign.md",)
    root = Path(__file__).resolve().parents[3] / "src" / "research" / "engine_campaign"
    for path in root.glob("*.py"):
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("from research.collatz") or stripped.startswith("import research.collatz"):
                raise AssertionError(f"{path.name} imports research.collatz")


def test_baseline_corpus_saturates_digit_fold():
    corpus = seed_baseline_corpus()
    names = {item.target for item in corpus.records}
    assert "operator_dynamics_benchmark" in names
    fold_fp = next(item.fingerprint for item in corpus.records if item.target == "operator_dynamics_benchmark")
    assert family_status_for(fold_fp, corpus.records) is FamilyStatus.SATURATED
    syracuse = next(item for item in corpus.records if item.target == "syracuse")
    assert not core_match(syracuse.fingerprint, fold_fp)
    assert syracuse.decision is ResearchDecision.CONTINUE


def test_campaign_runs_unmodified_loop():
    corpus, report = run_campaign()
    for m, r in FAMILY_PAIRS:
        summary = report.by_target(f"mx_plus_r_{m}_{r}")
        assert summary.census_kind == "PARAMETERIZED_CENSUS"
        assert summary.family is not None
        assert summary.family.get("p") == m
        assert summary.family.get("r") == r
        assert summary.family.get("base") == 2
        assert "piecewise_affine" not in summary.skipped

    three = report.by_target("mx_plus_r_3_1")
    five = report.by_target("mx_plus_r_5_1")
    assert three.family is not None and five.family is not None
    assert three.family.get("p") == 3 and three.family.get("r") == 1
    assert five.family.get("p") == 5 and five.family.get("r") == 1
    assert five.extra.get("compare_3_1", {}).get("seed_27_cyclic") is True
    assert five.extra.get("claim_discipline")

    euclid = report.by_target("euclidean_quotient")
    assert "piecewise_affine" in euclid.skipped
    assert euclid.fingerprint.get("state_space_type") == "INTEGER_VECTOR"
    assert euclid.extra.get("c1_gated") is (euclid.decision == ResearchDecision.ENGINE_LIMITATION.value)

    fold_fp = next(
        item.fingerprint
        for item in corpus.records
        if item.target == "operator_dynamics_benchmark"
    )
    assert family_status_for(fold_fp, corpus.records) in {
        FamilyStatus.SATURATED,
        FamilyStatus.EXHAUSTED,
    }
    for m, r in ((3, 1), (5, 3), (7, 1)):
        summary = report.by_target(f"mx_plus_r_{m}_{r}")
        fp = next(item.fingerprint for item in corpus.records if item.target == summary.target)
        assert not core_match(fp, fold_fp)
    euclid_fp = next(item.fingerprint for item in corpus.records if item.target == "euclidean_quotient")
    assert not core_match(euclid_fp, fold_fp)
    assert euclid.fingerprint.get("piecewise_affine_structure") in {
        "PARAMETERIZED",
        "FINITE",
    }
    assert euclid.fingerprint.get("affine_control_type") in {
        "MATRIX_PARAMETERIZED",
        "VECTOR",
    }

    assert report.selection
    assert report.selection[0].value > 0
    assert report.target_d_name == report.selection[0].name
    assert report.target_d_overridden is False
    spec_for_selection(report.target_d_name)
    d_summary = report.summaries[-1]
    assert d_summary.extra.get("role") == "target_d"
    assert d_summary.extra.get("selection")
