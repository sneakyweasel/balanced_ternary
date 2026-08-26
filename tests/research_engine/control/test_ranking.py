"""Phase-0 ranking falsifier: exact templates, not an attack."""

from __future__ import annotations

from pathlib import Path

from research_engine.control.baseline import load_v2_3_baseline, verify_manifest, sha256_file
from research_engine.control.proposals import assert_not_executable
from research_engine.control.ranking import (
    NEGATIVE_CONTROL,
    ObservedTransition,
    Phase0Decision,
    RankingCandidate,
    RankingVerdict,
    TargetRankingReport,
    canonicalize_coeffs,
    candidate_grid,
    decide_phase0,
    falsify_target,
    integer_features,
    evaluate_candidate,
    updated_proposals,
)
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, run_named_attack
from research_engine.attacks.result import AttackContext
from tests.research_engine.core.test_planner import CountdownSpec


RANKING_SOURCE = (
    Path(__file__).resolve().parents[3] / "src" / "research_engine" / "control" / "ranking.py"
)


def _transition(src: int, img: int, *, digit_src: int, digit_img: int, note: str) -> ObservedTransition:
    return ObservedTransition(
        source=src,
        image=img,
        source_features=integer_features(src, digit=digit_src, residue=src % 2),
        image_features=integer_features(img, digit=digit_img, residue=img % 2),
        note=note,
    )


def _tag_like(length: int, grew: int = 1) -> ObservedTransition:
    src = 1 << length
    img = 1 << (length + grew)
    return ObservedTransition(
        source=src,
        image=img,
        source_features=integer_features(src, digit=length, residue=0),
        image_features=integer_features(img, digit=length + grew, residue=0),
        note="rewrite length",
    )


def test_canonicalize_identifies_scale_and_sign():
    assert canonicalize_coeffs(0, 0, 0) is None
    assert canonicalize_coeffs(1, 2, 0) == canonicalize_coeffs(2, 4, 0)
    assert canonicalize_coeffs(1, 2, 0) == canonicalize_coeffs(-1, -2, 0)
    assert canonicalize_coeffs(2, 4, 2) == (1, 2, 1)


def test_candidate_grid_is_finite_and_canonical():
    items = candidate_grid()
    coeffs = [item.coeffs for item in items]
    assert (0, 0, 0) not in coeffs
    assert len(coeffs) == len(set(coeffs))
    assert len(items) < 7**3
    for item in items:
        assert canonicalize_coeffs(*item.coeffs) == item.coeffs


def test_evaluate_is_exact_integer_and_source_has_no_float_verdict():
    features = integer_features(13, digit=4, residue=1)
    value = RankingCandidate(1, 1, 0).evaluate(features)
    assert type(value) is int
    source = RANKING_SOURCE.read_text(encoding="utf-8")
    assert "math.log" not in source
    assert " from math import log" not in source


def test_length_ranking_fails_on_nondecreasing_words():
    transitions = tuple(_tag_like(n) for n in range(2, 8))
    result = evaluate_candidate(RankingCandidate(0, 1, 0), transitions, exceptional=set())
    assert result.survived is False
    assert result.failure_class is not None
    assert result.failure_class.value == "LENGTH_NONDECREASE"


def test_negative_control_is_implausible_even_if_anti_rankings_survive_inequalities():
    transitions = tuple(_tag_like(n) for n in range(2, 8))
    report = falsify_target(
        NEGATIVE_CONTROL,
        transitions,
        available_features=("digit=word_length",),
        exceptional=(),
        is_negative_control=True,
    )
    assert report.classification is RankingVerdict.RANKING_IMPLAUSIBLE
    assert report.survivors == ()
    assert report.formalization_ready == "not_yet_formalization_ready"


def test_odd_to_odd_growth_needs_richer_state():
    transitions = (
        _transition(3, 5, digit_src=2, digit_img=3, note="juggler odd floor-power"),
        _transition(5, 11, digit_src=3, digit_img=4, note="juggler odd floor-power"),
        _transition(4, 2, digit_src=3, digit_img=2, note="juggler even square-root"),
    )
    report = falsify_target(
        "juggler_sequence",
        transitions,
        available_features=("digit=bit_length", "residue=n mod 2"),
        exceptional=(1,),
    )
    assert report.classification is RankingVerdict.RANKING_NEEDS_RICHER_STATE
    assert report.survivors == ()
    assert "odd" in " ".join(report.failure_mechanisms)


def test_phase0_decision_refine_on_structured_primary_failures():
    def _stub(name: str) -> TargetRankingReport:
        return TargetRankingReport(
            target=name,
            available_features=("digit",),
            candidate_count=1,
            transitions_tested=4,
            exceptional_set=(),
            exactness="int",
            survivors=(),
            failures=(),
            strongest=None,
            classification=RankingVerdict.RANKING_NEEDS_RICHER_STATE,
            failure_mechanisms=("growth",),
            lexicographic_proposal="piecewise",
            formalization_ready="not_yet_formalization_ready",
        )

    decision, _reason = decide_phase0(
        (
            _stub("juggler_sequence"),
            _stub("reverse_and_add_base3"),
            _stub("home_prime_49"),
        )
    )
    assert decision is Phase0Decision.REFINE


def test_updated_proposals_are_not_executable():
    report = TargetRankingReport(
        target="juggler_sequence",
        available_features=("digit",),
        candidate_count=1,
        transitions_tested=4,
        exceptional_set=("1",),
        exactness="int",
        survivors=(),
        failures=(),
        strongest=None,
        classification=RankingVerdict.RANKING_NEEDS_RICHER_STATE,
        failure_mechanisms=("odd floor-power branch increases magnitude, including odd-to-odd",),
        lexicographic_proposal="composed odd-then-even ranking",
        formalization_ready="not_yet_formalization_ready",
    )
    dossier = updated_proposals(report)
    assert [item.rank for item in dossier.proposals] == [1, 2, 3]
    spec = CountdownSpec()
    context = AttackContext()
    for proposal in dossier.proposals:
        assert proposal.attack_name not in DEFAULT_ATTACK_ORDER
        assert_not_executable(proposal.attack_name)
        try:
            run_named_attack(proposal.attack_name, spec, context)
            raise AssertionError(f"{proposal.attack_name} was executable")
        except KeyError:
            pass
    assert dossier.proposals[0].attack_name == "odd_even_composed_ranking"


def test_frozen_v23_seeds_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
