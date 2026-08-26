"""Phase-12 Juggler parity-drift falsifier: three pre-ranked candidates."""

from __future__ import annotations

from pathlib import Path

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.juggler_parity_drift import (
    MAX_DEPTH,
    WORD_EE,
    WORD_OOOEE,
    DriftClass,
    classify,
    evaluate_candidate,
    exact_negative_drift,
    make_sample,
    ranked_candidates,
    shortest_negative_word,
    updated_proposals,
)
from research_engine.control.proposals import assert_not_executable
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS, EXPERIMENTAL_ATTACKS


def test_exactly_three_pre_ranked_candidates_and_word_selection():
    items = ranked_candidates()
    assert len(items) == 3
    assert [item.rank for item in items] == [1, 2, 3]
    assert items[0].name == "one_step_increment_bounds"
    assert items[1].name == "oooee_conditional_contraction"
    assert items[2].name == "shortest_negative_block"
    assert items[1].parity_word == WORD_OOOEE
    assert shortest_negative_word() == WORD_EE == items[2].parity_word
    assert exact_negative_drift("EE") is True
    assert exact_negative_drift("OEE") is True
    assert exact_negative_drift("OOOE") is False
    assert exact_negative_drift("OOOEE") is True
    assert MAX_DEPTH == 5
    assert items[0].loot_eligible is False
    assert items[1].loot_eligible is True
    assert items[2].loot_eligible is False


def test_one_step_bounds_and_exceptional_one():
    odd = make_sample(3, 1)
    even = make_sample(4, 1)
    one = make_sample(1, 1)
    c1 = ranked_candidates()[0]
    assert c1.in_domain(odd) is True
    assert c1.holds(odd) is True
    assert c1.in_domain(even) is True
    assert c1.holds(even) is True
    assert c1.in_domain(one) is False
    assert one.image == 1


def test_candidates_evaluate_exactly_without_adaptive_words():
    samples = (
        make_sample(1, 1),
        make_sample(3, 1),
        make_sample(4, 1),
        make_sample(4, 2),
        make_sample(3, 5),
        make_sample(25, 5),
        make_sample(39, 5),
    )
    cands = ranked_candidates()
    one = evaluate_candidate(cands[0], samples)
    block = evaluate_candidate(cands[1], samples)
    shortest = evaluate_candidate(cands[2], samples)
    assert one.survived is True
    assert one.failure_class == "DEFINITIONAL_RESTATEMENT"
    assert block.survived is True
    assert block.checked == 3
    assert shortest.survived is True
    assert shortest.parity_word == "EE"
    classification, loot, _reason = classify((one, block, shortest), lean_proved=True)
    assert classification is DriftClass.PARITY_DRIFT_GREEN_LOOT
    assert loot == "PARITY_DRIFT_GREEN_LOOT"
    assert make_sample(3, 5).word == "OOOEE"
    assert make_sample(3, 5).image == 2
    assert make_sample(3, 5).image < 3


def test_oooee_counterexample_stops_and_classifies_refuted():
    fake = make_sample(3, 5)
    broken = type(fake)(source=3, path=(3, 5, 11, 36, 6, 100), word="OOOEE")
    cands = ranked_candidates()
    one = evaluate_candidate(cands[0], (make_sample(3, 1), make_sample(4, 1)))
    block = evaluate_candidate(cands[1], (broken,))
    shortest = evaluate_candidate(cands[2], (make_sample(4, 2),))
    assert block.survived is False
    assert block.counterexample is not None
    assert block.failure_class == "BLOCK_NOT_CONTRACTIVE"
    classification, loot, _reason = classify((one, block, shortest), lean_proved=False)
    assert classification is DriftClass.PARITY_DRIFT_REFUTED
    assert loot == "NO_NEW_LOOT"


def test_updated_proposals_raise_block_and_are_not_executable():
    dossier = updated_proposals(DriftClass.PARITY_DRIFT_GREEN_LOOT)
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "parity_drift_block"
    assert "parity_drift_block" not in DEFAULT_ATTACK_ORDER
    assert "juggler_parity_drift_phase12" not in DEFAULT_ATTACK_ORDER
    for name in names:
        assert name not in DEFAULT_ATTACK_ORDER
        assert name not in EXPERIMENTAL_ATTACKS
        assert_not_executable(name)


def test_engine_module_scope_safety():
    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "control", "juggler_parity_drift.py"
    ).read_text(encoding="utf-8")
    assert "from bt" not in text
    assert "import bt" not in text
    assert "from research." not in text
    assert "MAX_DEPTH = 5" in text
    assert "MAX_DEPTH = 6" not in text
    assert "class ParityAutomaton" not in text
    assert "def build_automaton" not in text
    assert "#E/#O" not in text
    assert "parity frequency" not in text.lower() or "not a parity-frequency" in text.lower()
    attack = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "attacks", "restricted_symbolic_composition.py"
    ).read_text(encoding="utf-8")
    assert "juggler_parity_drift" not in attack
    orchestrator = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "planner", "orchestrator.py"
    ).read_text(encoding="utf-8")
    assert "juggler_parity_drift_phase12" not in orchestrator
    assert "parity_drift_block" not in orchestrator


def test_frozen_v23_and_flood_order_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert DEFERRED_ATTACKS == ("symbolic",)
    assert "juggler_parity_drift_phase12" not in DEFAULT_ATTACK_ORDER
    assert "parity_drift_block" not in DEFAULT_ATTACK_ORDER
    assert "juggler_parity_drift_phase12" not in EXPERIMENTAL_ATTACKS
    assert EXPERIMENTAL_ATTACKS == frozenset(
        {"restricted_symbolic_composition", "odd_even_two_step_decrease"}
    )
