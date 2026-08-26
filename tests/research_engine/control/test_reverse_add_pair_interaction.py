"""Phase-6 reverse-add pair-interaction falsifier: three pre-ranked candidates."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.reverse_add_pair_interaction import (
    PairSample,
    ReversePairClass,
    classify,
    evaluate_candidate,
    pair_aggregates,
    pair_sums_lsd,
    ranked_candidates,
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
) -> PairSample:
    stats = pair_aggregates(pair_sums)
    return PairSample(
        source=source,
        image=image,
        w_source=w_source,
        len_source=len_source,
        len_image=len_image,
        pair_sums=pair_sums,
        p0=stats["p0"],
        p2=stats["p2"],
        p_plus=stats["p_plus"],
        p_minus=stats["p_minus"],
        r_last=stats["r_last"],
    )


def test_exactly_three_pre_ranked_candidates():
    items = ranked_candidates()
    assert len(items) == 3
    assert [item.rank for item in items] == [1, 2, 3]
    assert items[0].name == "cancellation_majority_blocks_growth"
    assert items[1].name == "pair_sign_imbalance_matches_successor_sign"
    assert items[2].name == "length_growth_requires_top_pair"


def test_pair_sums_are_deterministic_and_raw():
    assert pair_sums_lsd((), ()) == (0,)
    assert pair_sums_lsd((0,), (0,)) == (0,)
    assert pair_sums_lsd((1,), (1,)) == (2,)
    assert pair_sums_lsd((-1,), (-1,)) == (-2,)
    assert pair_sums_lsd((-1, 1), (1, -1)) == (0, 0)
    assert pair_sums_lsd((1, 0), (1,)) == (2, 0)
    assert pair_sums_lsd((1,), (1,)) == pair_sums_lsd((1,), (1,))
    stats = pair_aggregates((0, -2, 0))
    assert stats["p0"] == 2
    assert stats["p2"] == 1
    assert stats["p_plus"] == 0
    assert stats["p_minus"] == 1
    assert stats["r_last"] == 1


def test_candidates_evaluate_exactly_and_stop_at_first_counterexample():
    samples = (
        _sample(1, 2, w_source=1, len_source=1, len_image=2, pair_sums=(2,)),
        _sample(2, 0, w_source=-2, len_source=2, len_image=1, pair_sums=(0, 0)),
        _sample(5, -6, w_source=-11, len_source=3, len_image=3, pair_sums=(0, -2, 0)),
        _sample(-672, -448, w_source=224, len_source=7, len_image=7, pair_sums=(1, 1, -2, 1, 1, 1, -1)),
    )
    cands = ranked_candidates()
    cancel = evaluate_candidate(cands[0], samples)
    sign = evaluate_candidate(cands[1], samples)
    top = evaluate_candidate(cands[2], samples)
    assert cancel.survived is True
    assert sign.survived is False
    assert sign.failure_class == "SIGN_IMBALANCE_MISMATCH"
    assert sign.counterexample is not None
    assert sign.counterexample.source == -672
    assert top.survived is True
    classification, _reason = classify((cancel, sign, top))
    assert classification is ReversePairClass.REVERSE_PAIR_NEEDS_RICHER_STRUCTURE
    assert len(cands) == 3


def test_updated_proposals_keep_composition_lead_and_are_not_executable():
    dossier = updated_proposals(ReversePairClass.REVERSE_PAIR_NEEDS_RICHER_STRUCTURE)
    assert [item.rank for item in dossier.proposals] == [1, 2, 3]
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "reverse_pair_interaction" not in names
    for name in names:
        assert name not in DEFAULT_ATTACK_ORDER
        assert name not in EXPERIMENTAL_ATTACKS
        assert_not_executable(name)


def test_refuted_pair_is_not_kept_as_a_future_attack():
    dossier = updated_proposals(ReversePairClass.REVERSE_PAIR_REFUTED)
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "reverse_pair_interaction" not in names
    assert any("refuted" in note.lower() for note in dossier.notes)


def test_engine_module_does_not_import_bt_or_open_ranking():
    from pathlib import Path

    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "control", "reverse_add_pair_interaction.py"
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
    assert "reverse_pair_phase6" not in DEFAULT_ATTACK_ORDER
    assert "reverse_pair_interaction" not in DEFAULT_ATTACK_ORDER
    assert "reverse_pair_phase6" not in EXPERIMENTAL_ATTACKS
    assert "reverse_pair_interaction" not in EXPERIMENTAL_ATTACKS
