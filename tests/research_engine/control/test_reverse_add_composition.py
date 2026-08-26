"""Phase-4 reverse-add composition falsifiers: three pre-ranked candidates."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.reverse_add_composition import (
    ReverseCompositionClass,
    ReverseSample,
    classify,
    evaluate_candidate,
    ranked_candidates,
    updated_proposals,
)
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS, EXPERIMENTAL_ATTACKS


def _sample(
    source: int,
    mid: int,
    image: int,
    *,
    w_source: int,
    w_mid: int,
    len_source: int,
    len_mid: int,
    len_image: int,
) -> ReverseSample:
    return ReverseSample(
        source=source,
        mid=mid,
        image=image,
        w_source=w_source,
        w_mid=w_mid,
        len_source=len_source,
        len_mid=len_mid,
        len_image=len_image,
    )


def test_exactly_three_pre_ranked_candidates():
    items = ranked_candidates()
    assert len(items) == 3
    assert [item.rank for item in items] == [1, 2, 3]
    assert items[0].name == "reverse_cancellation"
    assert items[1].name == "two_step_sign_preservation"
    assert items[2].name == "two_step_length_plus_one"


def test_cancellation_and_sign_fail_on_one_to_zero():
    samples = (
        _sample(1, 2, 0, w_source=1, w_mid=-2, len_source=1, len_mid=2, len_image=1),
        _sample(2, 0, 0, w_source=-2, w_mid=0, len_source=2, len_mid=1, len_image=1),
        _sample(3, 4, 8, w_source=1, w_mid=4, len_source=2, len_mid=2, len_image=3),
    )
    cands = ranked_candidates()
    cancel = evaluate_candidate(cands[0], samples)
    sign = evaluate_candidate(cands[1], samples)
    length = evaluate_candidate(cands[2], samples)
    assert cancel.survived is False
    assert cancel.failure_class == "CANCELLATION_FAILURE"
    assert cancel.counterexample is not None
    assert cancel.counterexample.source == 1
    assert sign.survived is False
    assert sign.failure_class == "SIGN_REVERSAL"
    assert sign.counterexample is not None
    assert sign.counterexample.source == 1
    assert length.survived is True
    classification, _reason = classify((cancel, sign, length))
    assert classification is ReverseCompositionClass.REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE


def test_updated_proposals_are_not_executable_and_close_reverse_branch():
    dossier = updated_proposals(ReverseCompositionClass.REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE)
    assert [item.rank for item in dossier.proposals] == [1, 2, 3]
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "reverse_add_symbolic_composition" not in names
    for name in names:
        assert name not in DEFAULT_ATTACK_ORDER
        assert name not in EXPERIMENTAL_ATTACKS
        assert_not_executable(name)


def test_frozen_v23_and_flood_order_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert DEFERRED_ATTACKS == ("symbolic",)
    assert "reverse_add_composition_phase4" not in DEFAULT_ATTACK_ORDER
    assert "reverse_add_symbolic_composition" not in DEFAULT_ATTACK_ORDER
    assert "reverse_add_composition_phase4" not in EXPERIMENTAL_ATTACKS
