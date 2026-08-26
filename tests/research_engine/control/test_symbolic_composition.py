"""Phase-2 symbolic composition falsifiers: exact k=2 probes, not an attack."""

from __future__ import annotations

from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.control.proposals import assert_not_executable
from research_engine.control.symbolic_composition import (
    HOME,
    JUGGLER,
    REVERSE,
    CompositionSample,
    Phase2Decision,
    decide_phase2,
    falsify_home,
    falsify_juggler,
    falsify_reverse,
    floor_power,
    integer_two_step_lt_certificate,
    odd_even_two_step,
    updated_proposals,
)
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, run_named_attack
from research_engine.attacks.result import AttackContext
from tests.research_engine.core.test_planner import CountdownSpec


def _sample(source: int, mid: int, image: int, *, extra=None, note: str = "") -> CompositionSample:
    return CompositionSample(source=source, mid=mid, image=image, note=note, extra=extra or {})


def test_odd_even_two_step_excludes_odd_odd_and_even():
    assert odd_even_two_step(3) is None
    assert odd_even_two_step(8) is None
    assert odd_even_two_step(1) is None


def test_integer_obstruction_forbids_k_ge_n():
    assert floor_power(7) == 18
    assert odd_even_two_step(7) == 4
    assert integer_two_step_lt_certificate(7, 4)
    assert 4 < 7
    assert floor_power(13) == 46
    assert odd_even_two_step(13) == 6


def test_composed_decrease_on_synthetic_odd_even():
    samples = (
        _sample(7, 18, 4, note="odd-even"),
        _sample(13, 46, 6, note="odd-even"),
        _sample(15, 58, 7, note="odd-even"),
    )
    report = falsify_juggler(samples, lean_status="PROVED")
    assert report.target == JUGGLER
    assert report.composition_depth == 2
    assert report.classification == "SYMBOLIC_COMPOSITION_PROMISING"
    assert report.lean_status == "PROVED"
    assert report.counterexamples == ()
    assert report.checks[0].survived
    assert report.next_proposal == "odd_even_symbolic_composition"


def test_reverse_mixed_ascent_and_descent():
    samples = (
        _sample(1, 2, 0, extra={"len_source": 1, "len_image": 1}, note="collapse"),
        _sample(2, 4, 8, extra={"len_source": 2, "len_image": 2}, note="growth"),
        _sample(5, 10, 20, extra={"len_source": 2, "len_image": 3}, note="growth"),
    )
    report = falsify_reverse(samples)
    assert report.target == REVERSE
    assert report.classification == "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    assert report.lean_status == "NOT_YET_FORMALIZATION_READY"
    names = {item.name: item for item in report.checks}
    assert names["t2_lt"].survived is False
    assert names["t2_gt"].survived is False
    assert names["t2_lt"].counterexample is not None
    assert names["t2_gt"].counterexample is not None
    assert names["t2_lt"].counterexample.source == 2
    assert names["t2_gt"].counterexample.source == 1


def test_home_concat_length_needs_richer_structure():
    samples = (
        _sample(
            4,
            22,
            211,
            extra={
                "len_source": 1,
                "len_mid": 2,
                "len_image": 3,
                "omega_source": 2,
                "omega_mid": 2,
                "omega_image": 3,
                "mid_prime": 0,
                "image_prime": 0,
            },
        ),
        _sample(
            10,
            25,
            55,
            extra={
                "len_source": 2,
                "len_mid": 2,
                "len_image": 2,
                "omega_source": 2,
                "omega_mid": 2,
                "omega_image": 2,
                "mid_prime": 0,
                "image_prime": 0,
            },
        ),
        _sample(
            9,
            33,
            311,
            extra={
                "len_source": 1,
                "len_mid": 2,
                "len_image": 3,
                "omega_source": 2,
                "omega_mid": 2,
                "omega_image": 2,
                "mid_prime": 0,
                "image_prime": 0,
            },
        ),
    )
    report = falsify_home(samples)
    assert report.target == HOME
    assert report.classification == "HOME_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    names = {item.name: item for item in report.checks}
    assert names["t_decimal_length_gt"].survived is False
    assert names["t_decimal_length_gt"].counterexample is not None
    assert names["t_decimal_length_gt"].counterexample.source == 10


def test_phase2_decision_mixed_when_only_juggler_is_exact():
    juggler = falsify_juggler(
        (
            _sample(7, 18, 4),
            _sample(13, 46, 6),
            _sample(15, 58, 7),
        ),
        lean_status="PROVED",
    )
    reverse = falsify_reverse(
        (
            _sample(1, 2, 0, extra={"len_source": 1, "len_image": 1}),
            _sample(2, 4, 8, extra={"len_source": 2, "len_image": 2}),
            _sample(5, 10, 20, extra={"len_source": 2, "len_image": 3}),
        )
    )
    home = falsify_home(
        (
            _sample(
                4,
                22,
                211,
                extra={
                    "len_source": 1,
                    "len_mid": 2,
                    "len_image": 3,
                    "omega_source": 2,
                    "omega_mid": 2,
                    "omega_image": 3,
                    "mid_prime": 0,
                    "image_prime": 0,
                },
            ),
            _sample(
                10,
                25,
                55,
                extra={
                    "len_source": 2,
                    "len_mid": 2,
                    "len_image": 2,
                    "omega_source": 2,
                    "omega_mid": 2,
                    "omega_image": 2,
                    "mid_prime": 0,
                    "image_prime": 0,
                },
            ),
            _sample(
                9,
                33,
                311,
                extra={
                    "len_source": 1,
                    "len_mid": 2,
                    "len_image": 3,
                    "omega_source": 2,
                    "omega_mid": 2,
                    "omega_image": 2,
                    "mid_prime": 0,
                    "image_prime": 0,
                },
            ),
        )
    )
    decision, _reason = decide_phase2((juggler, reverse, home))
    assert decision is Phase2Decision.MIXED
    assert juggler.next_proposal == "odd_even_symbolic_composition"


def test_updated_proposals_are_not_executable():
    report = falsify_juggler(
        (
            _sample(7, 18, 4),
            _sample(13, 46, 6),
            _sample(15, 58, 7),
        ),
        lean_status="PROVED",
    )
    dossier = updated_proposals(report)
    spec = CountdownSpec()
    context = AttackContext()
    assert [item.rank for item in dossier.proposals] == [1, 2, 3]
    assert dossier.proposals[0].attack_name == "odd_even_symbolic_composition"
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
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "symbolic" not in DEFAULT_ATTACK_ORDER[-1]
    assert "odd_even_symbolic_composition" not in DEFAULT_ATTACK_ORDER
    assert "ranking_function_synthesis" not in DEFAULT_ATTACK_ORDER
