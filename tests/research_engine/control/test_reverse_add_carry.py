"""Phase-5 reverse-add carry falsifier: three pre-ranked one-step candidates."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.reverse_add_carry import (
    CarryClass,
    CarrySample,
    carry_chain_length,
    classify,
    evaluate_candidate,
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
    carry_chain: int,
) -> CarrySample:
    return CarrySample(
        source=source,
        image=image,
        w_source=w_source,
        len_source=len_source,
        len_image=len_image,
        carry_chain=carry_chain,
    )


def test_exactly_three_pre_ranked_candidates():
    items = ranked_candidates()
    assert len(items) == 3
    assert [item.rank for item in items] == [1, 2, 3]
    assert items[0].name == "carry_bounds_length_growth"
    assert items[1].name == "zero_carry_preserves_length"
    assert items[2].name == "positive_carry_forces_length_plus_one"


def test_carry_chain_length_is_deterministic():
    assert carry_chain_length((), final_carry=0) == 0
    assert carry_chain_length(((0, 0),), final_carry=0) == 0
    assert carry_chain_length(((0, 1),), final_carry=1) == 2
    assert carry_chain_length(((0, 0), (0, -1), (-1, 0)), final_carry=0) == 2
    assert carry_chain_length(((0, 1),), final_carry=1) == carry_chain_length(((0, 1),), final_carry=1)


def test_candidates_evaluate_exactly_and_stop_at_first_counterexample():
    samples = (
        _sample(1, 2, w_source=1, len_source=1, len_image=2, carry_chain=2),
        _sample(2, 0, w_source=-2, len_source=2, len_image=1, carry_chain=0),
        _sample(5, -6, w_source=-11, len_source=3, len_image=3, carry_chain=2),
    )
    cands = ranked_candidates()
    growth = evaluate_candidate(cands[0], samples)
    zero = evaluate_candidate(cands[1], samples)
    positive = evaluate_candidate(cands[2], samples)
    assert growth.survived is True
    assert growth.counterexample is None
    assert zero.survived is False
    assert zero.failure_class == "REVERSAL_DEPENDENCE"
    assert zero.counterexample is not None
    assert zero.counterexample.source == 2
    assert zero.checked == 1
    assert positive.survived is False
    assert positive.failure_class == "LENGTH_DECOUPLING"
    assert positive.counterexample is not None
    assert positive.counterexample.source == 5
    classification, _reason = classify((growth, zero, positive))
    assert classification is CarryClass.CARRY_NEEDS_RICHER_STATE
    assert len(cands) == 3


def test_updated_proposals_keep_composition_lead_and_are_not_executable():
    dossier = updated_proposals(CarryClass.CARRY_NEEDS_RICHER_STATE)
    assert [item.rank for item in dossier.proposals] == [1, 2, 3]
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "carry_structure_analysis" not in names
    assert "balanced_ternary_carry_attack" not in names
    for name in names:
        assert name not in DEFAULT_ATTACK_ORDER
        assert name not in EXPERIMENTAL_ATTACKS
        assert_not_executable(name)


def test_refuted_carry_is_not_kept_as_a_future_attack():
    dossier = updated_proposals(CarryClass.CARRY_REFUTED)
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "carry_structure_analysis" not in names
    assert any("refuted" in note.lower() for note in dossier.notes)


def test_engine_module_does_not_import_bt_or_open_ranking():
    from pathlib import Path

    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "control", "reverse_add_carry.py"
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
    assert "carry_phase5" not in DEFAULT_ATTACK_ORDER
    assert "balanced_ternary_carry_attack" not in DEFAULT_ATTACK_ORDER
    assert "carry_phase5" not in EXPERIMENTAL_ATTACKS
    assert "balanced_ternary_carry_attack" not in EXPERIMENTAL_ATTACKS
