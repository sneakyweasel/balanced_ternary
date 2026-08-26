"""Phase-8 reverse-add involution falsifier: three pre-ranked candidates."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.reverse_add_involution import (
    FORBIDDEN_STATISTIC_KEYS,
    InvolutionSample,
    ReverseInvolutionClass,
    classify,
    evaluate_candidate,
    ranked_candidates,
    reverse_gap_from_msd,
    updated_proposals,
)
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS, EXPERIMENTAL_ATTACKS


def _sample(
    source: int,
    image: int,
    *,
    w_source: int,
    w_image: int,
    ww_source: int,
    len_source: int,
    len_image: int,
    gap_source: int,
    gap_image: int,
    msd_source: int,
    msd_w: int,
    msd_t: int,
) -> InvolutionSample:
    return InvolutionSample(
        source=source,
        image=image,
        w_source=w_source,
        w_image=w_image,
        ww_source=ww_source,
        len_source=len_source,
        len_image=len_image,
        gap_source=gap_source,
        gap_image=gap_image,
        msd_source=msd_source,
        msd_w=msd_w,
        msd_t=msd_t,
    )


def test_exactly_three_pre_ranked_candidates():
    items = ranked_candidates()
    assert len(items) == 3
    assert [item.rank for item in items] == [1, 2, 3]
    assert items[0].name == "reverse_sum_residual_bound"
    assert items[1].name == "successor_reverse_gap_length_bound"
    assert items[2].name == "successor_msd_from_operand_pair"


def test_reverse_gap_from_msd_is_l1_and_even_on_palindrome():
    assert reverse_gap_from_msd((0,)) == 0
    assert reverse_gap_from_msd((1,)) == 0
    assert reverse_gap_from_msd((1, -1)) == 4
    assert reverse_gap_from_msd((-1,)) == 0


def test_anti_tautology_sample_has_no_reconstruction_keys():
    item = _sample(
        1, 2, w_source=1, w_image=-2, ww_source=1,
        len_source=1, len_image=2, gap_source=0, gap_image=4,
        msd_source=1, msd_w=1, msd_t=1,
    )
    keys = set(item.as_dict())
    assert not (keys & FORBIDDEN_STATISTIC_KEYS)
    assert "t_squared" not in keys
    assert "mid" not in keys


def test_candidates_evaluate_exactly_and_stop_at_first_counterexample():
    samples = (
        _sample(1, 2, w_source=1, w_image=-2, ww_source=1, len_source=1, len_image=2, gap_source=0, gap_image=4, msd_source=1, msd_w=1, msd_t=1),
        _sample(2, 0, w_source=-2, w_image=0, ww_source=2, len_source=2, len_image=1, gap_source=4, gap_image=0, msd_source=1, msd_w=-1, msd_t=0),
        _sample(5, -6, w_source=-11, w_image=2, ww_source=5, len_source=3, len_image=3, gap_source=4, gap_image=2, msd_source=1, msd_w=-1, msd_t=-1),
    )
    cands = ranked_candidates()
    residual = evaluate_candidate(cands[0], samples)
    gap = evaluate_candidate(cands[1], samples)
    msd = evaluate_candidate(cands[2], samples)
    assert residual.survived is False
    assert residual.failure_class == "INVOLUTION_RESIDUAL_MISMATCH"
    assert residual.counterexample is not None
    assert residual.counterexample.source == 1
    assert gap.survived is False
    assert gap.failure_class == "SUCCESSOR_REVERSAL_UNCONTROLLED"
    assert gap.counterexample is not None
    assert gap.counterexample.source == 1
    assert msd.survived is True
    classification, _reason = classify((residual, gap, msd))
    assert classification is ReverseInvolutionClass.REVERSE_INVOLUTION_REFUTED
    assert len(cands) == 3


def test_updated_proposals_keep_composition_and_are_not_executable():
    dossier = updated_proposals(ReverseInvolutionClass.REVERSE_INVOLUTION_REFUTED)
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "reverse_involution_structure" not in names
    assert any("not_sufficient" in note for note in dossier.notes)
    for name in names:
        assert name not in DEFAULT_ATTACK_ORDER
        assert name not in EXPERIMENTAL_ATTACKS
        assert_not_executable(name)


def test_engine_module_does_not_import_bt_or_open_ranking():
    from pathlib import Path

    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "control", "reverse_add_involution.py"
    ).read_text(encoding="utf-8")
    assert "from bt" not in text
    assert "import bt" not in text
    assert "research.residuals" not in text
    assert "research_engine.control.ranking" not in text
    assert "def test_" not in text


def test_frozen_v23_and_flood_order_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert DEFERRED_ATTACKS == ("symbolic",)
    assert "reverse_involution_phase8" not in DEFAULT_ATTACK_ORDER
    assert "reverse_involution_structure" not in DEFAULT_ATTACK_ORDER
    assert "reverse_involution_phase8" not in EXPERIMENTAL_ATTACKS
    assert "reverse_involution_structure" not in EXPERIMENTAL_ATTACKS
