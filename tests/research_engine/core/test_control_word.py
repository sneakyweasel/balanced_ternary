"""Control-word composition of certified affine families. Ground truth lives here."""

from __future__ import annotations

from pathlib import Path

from research_engine.attacks.control_word import (
    ControlWordAttack,
    compose_affine_steps,
    cycle_constraint,
    subsequent_k_impossible,
)
from research_engine.attacks.piecewise_affine import PiecewiseAffineCensusAttack
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.hidden_piecewise import (
    HiddenInvolutionESpec,
    HiddenParityCarrySpec,
    HiddenPositiveDoubleSpec,
    HiddenPowerClearDSpec,
)
from research_engine.planner.orchestrator import AttackPlanner, DEFAULT_ATTACK_ORDER, run_named_attack
from tests.research_engine.core.test_planner import CountdownSpec


def _source_text() -> str:
    root = Path(__file__).resolve().parents[3]
    return "\n".join(
        (root / "src" / "research_engine" / "attacks" / name).read_text(encoding="utf-8")
        for name in ("control_word.py", "parameter_domain.py", "piecewise_affine.py")
    )


def _control_word(spec) -> object:
    report = AttackPlanner().run(spec, spec.attack_context())
    return next(item for item in report.results if item.name == "control_word")


def test_attack_source_does_not_seed_collatz_structure():
    text = _source_text()
    lowered = text.lower()
    assert "collatz" not in lowered
    assert "syracuse" not in lowered
    assert "3 * n + 1" not in text
    assert "v_2(3" not in text


def test_cleared_composition_and_cycle_are_generic_algebra():
    assert compose_affine_steps(()) == (1, 1, 0)
    assert compose_affine_steps(((2, 3, 1),)) == (2, 3, 1)
    assert compose_affine_steps(((2, 3, 1), (4, 3, 1))) == (8, 9, 5)
    constraint = cycle_constraint(8, 9, 5)
    assert constraint.kind == "CYCLE_CONSTRAINT"
    assert constraint.left == -1
    assert constraint.right == 5
    assert constraint.residue == 0
    assert subsequent_k_impossible(1, 1, 2, 0) is True
    assert subsequent_k_impossible(1, 1, 2, 1) is False
    assert subsequent_k_impossible(3, 1, 2, 0) is True
    assert subsequent_k_impossible(3, 1, 2, 1) is False


def test_countdown_is_inapplicable_without_certificate():
    spec = CountdownSpec()
    attack = ControlWordAttack()
    assert attack.applicable(spec, AttackContext()) is False


def test_a_finite_alphabet_composes_without_ground_truth_on_the_spec():
    spec = HiddenParityCarrySpec()
    result = _control_word(spec)
    assert result.status in {AttackStatus.SUPPORTED, AttackStatus.OBSERVATION}
    assert result.evidence.get("reconstructed_affine") is None
    relations = result.evidence.get("relations") or ()
    assert relations
    census = PiecewiseAffineCensusAttack().run(spec, spec.attack_context())
    branches = census.evidence.get("branches") or ()
    assert len(branches) == 2
    by_index = {index: (int(item["q"]), int(item["p"]), int(item["r"])) for index, item in enumerate(branches)}
    for item in relations:
        word = tuple(item["word"]["parameters"])
        steps = tuple((by_index[k][0], by_index[k][1], by_index[k][2]) for k in word)
        expected = compose_affine_steps(steps)
        assert (item["a"], item["b"], item["c"]) == expected


def test_b_c_unbounded_domain_coupled_and_d_impossible_later_zero():
    spec = HiddenPowerClearDSpec()
    result = _control_word(spec)
    family = result.evidence.get("family")
    assert family is not None
    assert family.get("p") == 1 and family.get("r") == 1
    relations = {tuple(item["word"]["parameters"]): item for item in result.evidence.get("relations") or ()}
    assert relations
    word = next(iter(relations))
    steps = tuple(
        (int(family.get("base") or family["q_base"]) ** k, int(family["p"]), int(family["r"]))
        for k in word
    )
    expected = compose_affine_steps(steps)
    got = relations[word]
    assert (got["a"], got["b"], got["c"]) == expected
    impossible = {tuple(item) for item in result.evidence.get("impossible_words") or ()}
    assert any(len(word) >= 2 and word[-1] == 0 for word in impossible)


def test_e_involution_closes_a_cycle():
    spec = HiddenInvolutionESpec()
    result = _control_word(spec)
    length_two = [
        item
        for item in result.evidence.get("relations") or ()
        if item["word"]["length"] == 2
    ]
    assert length_two
    identity = [item for item in length_two if item["a"] == item["b"] and item["c"] == 0]
    assert identity
    identity_words = {tuple(item["word"]["parameters"]) for item in identity}
    realizable = [
        item
        for item in result.evidence.get("realizability") or ()
        if item.get("status") == "REALIZABLE_FOR_SOME_SEED"
        and tuple(item["word"]) in identity_words
    ]
    assert realizable
    assert any(item.get("seeds") for item in realizable)


def test_f_algebraic_cycle_candidate_misses_the_nonnegative_domain():
    spec = HiddenPositiveDoubleSpec()
    result = _control_word(spec)
    length_one = [
        item
        for item in result.evidence.get("realizability") or ()
        if len(item["word"]) == 1
    ]
    assert length_one
    assert any(item.get("cycle_candidate") == -1 for item in length_one)
    seeds = [seed for item in length_one for seed in item.get("seeds", ())]
    assert all(seed >= 0 for seed in seeds)
    assert -1 not in seeds


def test_named_attack_chains_census_and_domain():
    spec = HiddenPowerClearDSpec()
    result = run_named_attack("control_word", spec, spec.attack_context())
    assert result.name == "control_word"
    assert result.evidence.get("relations")


def test_planner_order_and_no_affine_injection():
    spec = HiddenPowerClearDSpec()
    context = spec.attack_context()
    assert context.affine is None
    report = AttackPlanner().run(spec, context)
    names = [item.name for item in report.results]
    assert names[0] == "reconnaissance"
    assert names[1] == "piecewise_affine"
    assert names[2] == "parameter_domain"
    assert names[3] == "control_word"
    assert names[4] == "control_obstruction"
    assert DEFAULT_ATTACK_ORDER.index("control_word") == DEFAULT_ATTACK_ORDER.index("parameter_domain") + 1
    composed = next(item for item in report.results if item.name == "control_word")
    assert composed.evidence.get("reconstructed_affine") is None
    assert spec.attack_context().affine is None
    skipped = {item.attack for item in report.skipped}
    assert "block" in skipped
    assert "spectral" in skipped


def test_lean_composition_has_no_sorry():
    path = Path(__file__).resolve().parents[3] / "formal" / "Problems" / "Engine" / "ControlWord.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert "compose_two_affine" in text
    assert "cycle_of_composed" in text
    assert "hiddenInvolutionE_period2" in text
