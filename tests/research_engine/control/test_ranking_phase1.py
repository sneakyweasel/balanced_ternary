"""Phase-1 enriched ranking falsifiers: exact templates, not an attack."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, verify_manifest, sha256_file
from research_engine.control.proposals import assert_not_executable
from research_engine.control.ranking import ObservedTransition, integer_features
from research_engine.control.ranking_phase1 import (
    HOME,
    JUGGLER,
    REVERSE,
    LinearCandidate,
    Phase1Decision,
    canonicalize_coeffs_n,
    decide_phase1,
    falsify_home_piecewise,
    falsify_juggler_composed,
    falsify_reverse_gap,
    reverse_gap_grid,
    updated_proposals,
)
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, run_named_attack
from research_engine.attacks.result import AttackContext
from tests.research_engine.core.test_planner import CountdownSpec


def _step(src: int, img: int, *, digit_src: int, digit_img: int, extra_src=None, extra_img=None, note: str):
    return ObservedTransition(
        source=src,
        image=img,
        source_features=integer_features(
            src, digit=digit_src, residue=src % 2, extra=extra_src or {}
        ),
        image_features=integer_features(
            img, digit=digit_img, residue=img % 2, extra=extra_img or {}
        ),
        note=note,
    )


def test_canonicalize_n_identifies_scale_and_sign():
    assert canonicalize_coeffs_n((0, 0, 0, 0)) is None
    assert canonicalize_coeffs_n((1, 0, 0, 2)) == canonicalize_coeffs_n((2, 0, 0, 4))
    assert canonicalize_coeffs_n((1, 0, 0, 2)) == canonicalize_coeffs_n((-1, 0, 0, -2))


def test_reverse_gap_grid_is_tiny_and_not_four_dimensional_exhaustive():
    items = reverse_gap_grid()
    assert len(items) < 50
    assert all(item.keys[-1] == "reverse_gap" for item in items)


def test_composed_size_ranking_survives_contracting_macros():
    transitions = (
        _step(7, 4, digit_src=3, digit_img=3, note="juggler odd-even composed k=2"),
        _step(13, 6, digit_src=4, digit_img=3, note="juggler odd-even composed k=2"),
        _step(15, 7, digit_src=4, digit_img=3, note="juggler odd-even composed k=2"),
        _step(21, 9, digit_src=5, digit_img=4, note="juggler odd-even composed k=2"),
    )
    report = falsify_juggler_composed(transitions, odd_odd_count=2)
    assert report.classification == "COMPOSED_RANKING_PROMISING"
    assert report.transition_depth == 2
    assert report.survivors


def test_reverse_gap_fails_when_a_palindrome_maps_away():
    transitions = (
        _step(
            1,
            2,
            digit_src=1,
            digit_img=2,
            extra_src={"reverse_gap": 0},
            extra_img={"reverse_gap": 4},
            note="reverse digit_reversal",
        ),
        _step(
            4,
            8,
            digit_src=2,
            digit_img=2,
            extra_src={"reverse_gap": 2},
            extra_img={"reverse_gap": 4},
            note="reverse digit_reversal",
        ),
        _step(
            5,
            10,
            digit_src=2,
            digit_img=3,
            extra_src={"reverse_gap": 2},
            extra_img={"reverse_gap": 2},
            note="reverse digit_reversal",
        ),
    )
    report = falsify_reverse_gap(transitions)
    assert report.classification == "REVERSE_GAP_IMPLAUSIBLE"
    assert report.survivors == ()
    assert any("palindrome" in item.lower() for item in report.failure_mechanisms)


def test_piecewise_concat_growth_needs_richer_state():
    transitions = (
        _step(
            4,
            22,
            digit_src=1,
            digit_img=2,
            extra_src={"factor_count": 2, "omega": 1},
            extra_img={"factor_count": 2, "omega": 2},
            note="home factor concat",
        ),
        _step(
            8,
            222,
            digit_src=1,
            digit_img=3,
            extra_src={"factor_count": 3, "omega": 1},
            extra_img={"factor_count": 3, "omega": 2},
            note="home factor concat",
        ),
        _step(
            9,
            33,
            digit_src=1,
            digit_img=2,
            extra_src={"factor_count": 2, "omega": 1},
            extra_img={"factor_count": 2, "omega": 2},
            note="home factor concat",
        ),
        _step(
            15,
            35,
            digit_src=2,
            digit_img=2,
            extra_src={"factor_count": 2, "omega": 2},
            extra_img={"factor_count": 2, "omega": 2},
            note="home factor concat",
        ),
    )
    report = falsify_home_piecewise(transitions)
    assert report.classification == "PIECEWISE_RANKING_NEEDS_RICHER_STATE"
    assert report.survivors == ()


def test_linear_candidate_is_exact_integer():
    features = integer_features(4, digit=1, residue=1, extra={"factor_count": 2, "omega": 1})
    value = LinearCandidate((1, 1, 0), ("digit", "factor_count", "omega")).evaluate(features)
    assert type(value) is int
    assert value == 3


def test_phase1_decision_mixed_when_only_one_branch_survives():
    composed = falsify_juggler_composed(
        (
            _step(7, 4, digit_src=3, digit_img=3, note="juggler odd-even composed k=2"),
            _step(13, 6, digit_src=4, digit_img=3, note="juggler odd-even composed k=2"),
            _step(15, 7, digit_src=4, digit_img=3, note="juggler odd-even composed k=2"),
        )
    )
    reverse = falsify_reverse_gap(
        (
            _step(
                1,
                2,
                digit_src=1,
                digit_img=2,
                extra_src={"reverse_gap": 0},
                extra_img={"reverse_gap": 4},
                note="reverse",
            ),
            _step(
                4,
                8,
                digit_src=2,
                digit_img=2,
                extra_src={"reverse_gap": 2},
                extra_img={"reverse_gap": 4},
                note="reverse",
            ),
            _step(
                5,
                10,
                digit_src=2,
                digit_img=3,
                extra_src={"reverse_gap": 2},
                extra_img={"reverse_gap": 2},
                note="reverse",
            ),
        )
    )
    home = falsify_home_piecewise(
        (
            _step(
                4,
                22,
                digit_src=1,
                digit_img=2,
                extra_src={"factor_count": 2, "omega": 1},
                extra_img={"factor_count": 2, "omega": 2},
                note="home",
            ),
            _step(
                8,
                222,
                digit_src=1,
                digit_img=3,
                extra_src={"factor_count": 3, "omega": 1},
                extra_img={"factor_count": 3, "omega": 2},
                note="home",
            ),
            _step(
                9,
                33,
                digit_src=1,
                digit_img=2,
                extra_src={"factor_count": 2, "omega": 1},
                extra_img={"factor_count": 2, "omega": 2},
                note="home",
            ),
            _step(
                15,
                35,
                digit_src=2,
                digit_img=2,
                extra_src={"factor_count": 2, "omega": 2},
                extra_img={"factor_count": 2, "omega": 2},
                note="home",
            ),
        )
    )
    decision, _reason = decide_phase1((composed, reverse, home))
    assert decision is Phase1Decision.MIXED
    assert composed.target == JUGGLER
    assert reverse.target == REVERSE
    assert home.target == HOME


def test_updated_proposals_are_not_executable():
    report = falsify_reverse_gap(
        (
            _step(
                1,
                2,
                digit_src=1,
                digit_img=2,
                extra_src={"reverse_gap": 0},
                extra_img={"reverse_gap": 4},
                note="reverse",
            ),
            _step(
                4,
                8,
                digit_src=2,
                digit_img=2,
                extra_src={"reverse_gap": 2},
                extra_img={"reverse_gap": 4},
                note="reverse",
            ),
            _step(
                5,
                10,
                digit_src=2,
                digit_img=3,
                extra_src={"reverse_gap": 2},
                extra_img={"reverse_gap": 2},
                note="reverse",
            ),
        )
    )
    dossier = updated_proposals(report)
    spec = CountdownSpec()
    context = AttackContext()
    assert [item.rank for item in dossier.proposals] == [1, 2, 3]
    for proposal in dossier.proposals:
        assert proposal.attack_name not in DEFAULT_ATTACK_ORDER
        assert_not_executable(proposal.attack_name)
        try:
            run_named_attack(proposal.attack_name, spec, context)
            raise AssertionError(f"{proposal.attack_name} was executable")
        except KeyError:
            pass


def test_frozen_v23_seeds_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert "ranking" not in DEFAULT_ATTACK_ORDER[-1]
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
