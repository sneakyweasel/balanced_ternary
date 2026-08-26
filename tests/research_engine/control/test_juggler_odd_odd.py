"""Phase-10 Juggler odd-odd k=2 falsifier: three pre-ranked candidates."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.juggler_odd_odd import (
    DEPTH,
    OddOddClass,
    OddOddSample,
    classify,
    evaluate_candidate,
    in_d_oe,
    in_d_oo,
    odd_even_two_step,
    odd_odd_two_step,
    ranked_candidates,
    updated_proposals,
)
from research_engine.control.proposals import assert_not_executable
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS, EXPERIMENTAL_ATTACKS


def _sample(source: int, mid: int, image: int) -> OddOddSample:
    return OddOddSample(source=source, mid=mid, image=image)


def test_exactly_three_pre_ranked_candidates():
    items = ranked_candidates()
    assert len(items) == 3
    assert [item.rank for item in items] == [1, 2, 3]
    assert items[0].name == "strict_two_step_growth"
    assert items[1].name == "thresholded_two_step_growth"
    assert items[2].name == "odd_cylinder_preservation"
    assert DEPTH == 2
    assert odd_odd_two_step.__doc__ is not None
    assert "exactly 2" in odd_odd_two_step.__doc__ or "Depth is exactly 2" in odd_odd_two_step.__doc__


def test_domain_separation_odd_even_versus_odd_odd():
    assert in_d_oo(1) is True
    assert in_d_oe(1) is False
    assert odd_odd_two_step(1) == 1
    assert in_d_oo(3) is True
    assert in_d_oe(3) is False
    assert odd_odd_two_step(3) == 11
    assert in_d_oo(5) is True
    assert odd_odd_two_step(5) == 36
    assert in_d_oe(7) is True
    assert in_d_oo(7) is False
    assert odd_even_two_step(7) is not None
    assert odd_even_two_step(7) < 7
    assert odd_odd_two_step(7) is None
    assert in_d_oe(13) is True
    assert in_d_oo(13) is False


def test_candidates_evaluate_exactly_and_stop_at_first_counterexample():
    samples = (
        _sample(1, 1, 1),
        _sample(3, 5, 11),
        _sample(5, 11, 36),
        _sample(9, 27, 140),
    )
    cands = ranked_candidates()
    strict = evaluate_candidate(cands[0], samples)
    growth = evaluate_candidate(cands[1], samples)
    preserve = evaluate_candidate(cands[2], samples)
    assert strict.survived is False
    assert strict.counterexample is not None
    assert strict.counterexample.source == 1
    assert strict.failure_class == "THRESHOLD_FAILURE"
    assert growth.survived is True
    assert preserve.survived is False
    assert preserve.counterexample is not None
    assert preserve.counterexample.source == 5
    assert preserve.failure_class == "PARITY_DOMAIN_LEAK"
    classification, _reason = classify((strict, growth, preserve))
    assert classification is OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT
    assert len(cands) == 3


def test_updated_proposals_raise_odd_odd_and_are_not_executable():
    dossier = updated_proposals(OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT)
    names = [item.attack_name for item in dossier.proposals]
    assert names[0] == "odd_odd_symbolic_composition"
    assert "odd_odd_branch_composition" not in names
    for name in names:
        assert name not in DEFAULT_ATTACK_ORDER
        assert name not in EXPERIMENTAL_ATTACKS
        assert_not_executable(name)


def test_engine_module_does_not_import_bt_or_mutate_odd_even_attack():
    from pathlib import Path

    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "control", "juggler_odd_odd.py"
    ).read_text(encoding="utf-8")
    assert "from bt" not in text
    assert "import bt" not in text
    assert "composition_depth = 3" not in text
    assert "DEPTH = 3" not in text
    assert "DEPTH = 2" in text
    attack = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "attacks", "restricted_symbolic_composition.py"
    ).read_text(encoding="utf-8")
    assert "odd_odd_two_step" not in attack
    assert "RULE_NAME = \"odd_even_two_step_decrease\"" in attack


def test_frozen_v23_and_flood_order_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert DEFERRED_ATTACKS == ("symbolic",)
    assert "juggler_odd_odd_phase10" not in DEFAULT_ATTACK_ORDER
    assert "odd_odd_branch_composition" not in DEFAULT_ATTACK_ORDER
    assert "odd_odd_symbolic_composition" not in DEFAULT_ATTACK_ORDER
    assert "juggler_odd_odd_phase10" not in EXPERIMENTAL_ATTACKS
    assert EXPERIMENTAL_ATTACKS == frozenset(
        {"restricted_symbolic_composition", "odd_even_two_step_decrease"}
    )
