"""Phase-11 Juggler macro-grammar falsifier: three pre-ranked candidates."""

from __future__ import annotations

from pathlib import Path

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.juggler_macro import (
    DEPTH,
    EXPERIMENT_NAME,
    MacroClass,
    MacroSample,
    classify,
    complementary_odd_ge3,
    evaluate_candidate,
    ranked_candidates,
    updated_proposals,
)
from research_engine.control.juggler_odd_odd import in_d_oe, in_d_oo, odd_even_two_step, odd_odd_two_step
from research_engine.control.proposals import assert_not_executable
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS, EXPERIMENTAL_ATTACKS


def _sample(source: int, mid: int, image: int, branch: str) -> MacroSample:
    return MacroSample(source=source, mid=mid, image=image, branch=branch)


def test_exactly_three_pre_ranked_candidates():
    items = ranked_candidates()
    assert len(items) == 3
    assert [item.rank for item in items] == [1, 2, 3]
    assert items[0].name == "combined_direction_law"
    assert items[1].name == "branch_determines_t2_parity"
    assert items[2].name == "contraction_exits_odd_macro"
    assert DEPTH == 2
    assert EXPERIMENT_NAME == "juggler_macro_phase11"


def test_branch_partition_and_exceptional_one():
    assert in_d_oo(1) is True
    assert in_d_oe(1) is False
    assert complementary_odd_ge3(1) is False
    assert odd_odd_two_step(1) == 1
    for n in range(3, 41, 2):
        assert complementary_odd_ge3(n) is True
        assert (in_d_oe(n) and not in_d_oo(n)) or (in_d_oo(n) and not in_d_oe(n))
    assert in_d_oe(7) is True
    assert odd_even_two_step(7) == 4
    assert odd_even_two_step(7) < 7
    assert in_d_oo(3) is True
    assert odd_odd_two_step(3) == 11
    assert odd_odd_two_step(3) > 3
    assert in_d_oo(5) is True
    assert odd_odd_two_step(5) == 36


def test_candidates_evaluate_exactly_and_stop_at_first_counterexample():
    samples = (
        _sample(1, 1, 1, "O"),
        _sample(3, 5, 11, "O"),
        _sample(5, 11, 36, "O"),
        _sample(7, 18, 4, "E"),
        _sample(15, 58, 7, "E"),
    )
    cands = ranked_candidates()
    combined = evaluate_candidate(cands[0], samples)
    parity = evaluate_candidate(cands[1], samples)
    survival = evaluate_candidate(cands[2], samples)
    assert combined.survived is True
    assert combined.failure_class == ""
    assert parity.survived is False
    assert parity.counterexample is not None
    assert parity.counterexample.source == 5
    assert parity.failure_class == "MACRO_PARITY_NOT_DETERMINISTIC"
    assert survival.survived is False
    assert survival.counterexample is not None
    assert survival.counterexample.source == 15
    assert survival.failure_class == "DIRECTION_SURVIVAL_DECOUPLING"
    classification, _reason = classify((combined, parity, survival))
    assert classification is MacroClass.MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE
    assert len(cands) == 3


def test_updated_proposals_move_off_juggler_micro_attacks():
    dossier = updated_proposals(MacroClass.MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE)
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "basin_preimage_grammar"
    assert names[1] == "odd_odd_symbolic_composition"
    assert "juggler_macro_grammar" not in names
    assert "macro_state_needs_richer_information" in dossier.notes
    assert "mx_plus_r_7x1_class_obstruction" in dossier.proposals[0].mathematical_target
    for name in names:
        assert name not in DEFAULT_ATTACK_ORDER
        assert name not in EXPERIMENTAL_ATTACKS
        assert_not_executable(name)


def test_engine_module_does_not_import_bt_or_build_automaton():
    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "control", "juggler_macro.py"
    ).read_text(encoding="utf-8")
    assert "from bt" not in text
    assert "import bt" not in text
    assert "from research." not in text
    assert "composition_depth = 3" not in text
    assert "DEPTH = 3" not in text
    assert "DEPTH = 2" in text
    assert "class ParityAutomaton" not in text
    assert "def build_automaton" not in text
    assert "DEFAULT_ATTACK_ORDER" in text
    attack = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "attacks", "restricted_symbolic_composition.py"
    ).read_text(encoding="utf-8")
    assert "juggler_macro" not in attack
    assert "RULE_NAME = \"odd_even_two_step_decrease\"" in attack
    orchestrator = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "planner", "orchestrator.py"
    ).read_text(encoding="utf-8")
    assert "juggler_macro_phase11" not in orchestrator
    assert "juggler_macro_grammar" not in orchestrator


def test_frozen_v23_and_flood_order_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert DEFERRED_ATTACKS == ("symbolic",)
    assert EXPERIMENT_NAME not in DEFAULT_ATTACK_ORDER
    assert "juggler_macro_grammar" not in DEFAULT_ATTACK_ORDER
    assert "juggler_macro_phase11" not in EXPERIMENTAL_ATTACKS
    assert EXPERIMENTAL_ATTACKS == frozenset(
        {"restricted_symbolic_composition", "odd_even_two_step_decrease"}
    )
