"""Phase-7 weighted reverse-pair falsifier: three pre-ranked positional summaries."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.reverse_add_weighted_pair import (
    FORBIDDEN_STATISTIC_KEYS,
    WeightedPairClass,
    WeightedSample,
    assert_not_reconstruction,
    classify,
    evaluate_candidate,
    positional_profile,
    ranked_candidates,
    tautology_checks,
    updated_proposals,
)
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS, EXPERIMENTAL_ATTACKS


def _sample(
    source: int,
    image: int,
    *,
    w_source: int,
    len_source: int,
    len_image: int,
    pair_sums: tuple[int, ...],
) -> WeightedSample:
    stats = positional_profile(pair_sums)
    return WeightedSample(
        source=source,
        image=image,
        w_source=w_source,
        len_source=len_source,
        len_image=len_image,
        pair_sums=pair_sums,
        h=stats["h"],
        sign_h=stats["sign_h"],
        m_plus=stats["m_plus"],
        m_minus=stats["m_minus"],
        h2=stats["h2"],
        sign_h2=stats["sign_h2"],
    )


def test_exactly_three_pre_ranked_candidates():
    items = ranked_candidates()
    assert len(items) == 3
    assert [item.rank for item in items] == [1, 2, 3]
    assert items[0].name == "highest_nonzero_pair_determines_sign"
    assert items[1].name == "highest_positive_vs_highest_negative"
    assert items[2].name == "highest_mag2_determines_sign"


def test_positional_statistics_and_zero_handling():
    empty = positional_profile((0, 0))
    assert empty["h"] is None
    assert empty["m_plus"] is None
    assert empty["m_minus"] is None
    assert empty["h2"] is None
    pal = positional_profile((2,))
    assert pal["h"] == 0 and pal["sign_h"] == 1 and pal["h2"] == 0
    mixed = positional_profile((-2, 1))
    assert mixed["h"] == 1 and mixed["sign_h"] == 1
    assert mixed["m_plus"] == 1 and mixed["m_minus"] == 0
    assert mixed["h2"] == 0 and mixed["sign_h2"] == -1
    padded = positional_profile((2, 0))
    assert padded["h"] == 0
    assert "weighted_sum" not in mixed
    assert_not_reconstruction(mixed)


def test_anti_tautology_rejects_full_sum():
    checks = tautology_checks()
    assert checks["candidates_reconstruct_T"] is False
    assert checks["coarser_than_full_sum"] is True
    sample = _sample(1, 2, w_source=1, len_source=1, len_image=2, pair_sums=(2,))
    keys = set(sample.as_dict())
    assert not (keys & FORBIDDEN_STATISTIC_KEYS)
    assert "pair_sums" in keys
    assert "h" in keys


def test_candidates_evaluate_exactly_and_stop_at_first_counterexample():
    samples = (
        _sample(1, 2, w_source=1, len_source=1, len_image=2, pair_sums=(2,)),
        _sample(2, 0, w_source=-2, len_source=2, len_image=1, pair_sums=(0, 0)),
        _sample(5, -6, w_source=-11, len_source=3, len_image=3, pair_sums=(0, -2, 0)),
        _sample(6, 4, w_source=-2, len_source=3, len_image=2, pair_sums=(-2, 1)),
        _sample(-672, -448, w_source=224, len_source=7, len_image=7, pair_sums=(-1, 1, 1, -2, 1, 1, -1)),
    )
    cands = ranked_candidates()
    top = evaluate_candidate(cands[0], samples)
    dom = evaluate_candidate(cands[1], samples)
    mag2 = evaluate_candidate(cands[2], samples)
    assert top.survived is True
    assert dom.survived is True
    assert mag2.survived is False
    assert mag2.failure_class == "MULTI_POSITION_INTERFERENCE"
    assert mag2.counterexample is not None
    assert mag2.counterexample.source == 6
    classification, _reason = classify((top, dom, mag2))
    assert classification is WeightedPairClass.WEIGHTED_PAIR_PROMISING
    assert len(cands) == 3


def test_updated_proposals_keep_composition_lead_and_are_not_executable():
    dossier = updated_proposals(WeightedPairClass.WEIGHTED_PAIR_PROMISING)
    assert [item.rank for item in dossier.proposals] == [1, 2, 3]
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "weighted_reverse_pair_interaction" not in names
    for name in names:
        assert name not in DEFAULT_ATTACK_ORDER
        assert name not in EXPERIMENTAL_ATTACKS
        assert_not_executable(name)


def test_refuted_weighted_pair_is_not_kept_as_a_future_attack():
    dossier = updated_proposals(WeightedPairClass.WEIGHTED_PAIR_REFUTED)
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "weighted_reverse_pair_interaction" not in names
    assert any("insufficient" in note.lower() for note in dossier.notes)


def test_engine_module_does_not_import_bt_or_open_ranking():
    from pathlib import Path

    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "control", "reverse_add_weighted_pair.py"
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
    assert "reverse_pair_weighted_phase7" not in DEFAULT_ATTACK_ORDER
    assert "weighted_reverse_pair_interaction" not in DEFAULT_ATTACK_ORDER
    assert "reverse_pair_weighted_phase7" not in EXPERIMENTAL_ATTACKS
    assert "weighted_reverse_pair_interaction" not in EXPERIMENTAL_ATTACKS
