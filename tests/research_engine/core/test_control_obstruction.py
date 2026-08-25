"""Class-level control-word obstructions. Ground truth lives here."""

from __future__ import annotations

from pathlib import Path

from research_engine.attacks.control_obstruction import (
    ControlObstructionAttack,
    length_one_divisor_class,
    run_control_obstruction,
)
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.hidden_piecewise import (
    HiddenLargeFixedSpec,
    HiddenOddPrimeClearSpec,
    HiddenParityCarrySpec,
    HiddenPositiveDoubleSpec,
    HiddenPowerClearDSpec,
)
from research_engine.core.semantics import SearchScope
from research_engine.planner.orchestrator import AttackPlanner, DEFAULT_ATTACK_ORDER, run_named_attack
from tests.research_engine.core.test_planner import CountdownSpec


def _source_text() -> str:
    root = Path(__file__).resolve().parents[3]
    return (root / "src" / "research_engine" / "attacks" / "control_obstruction.py").read_text(
        encoding="utf-8"
    )


def _obstruction(spec) -> object:
    report = AttackPlanner().run(spec, spec.attack_context())
    return next(item for item in report.results if item.name == "control_obstruction")


def test_attack_source_does_not_seed_collatz_structure():
    text = _source_text()
    lowered = text.lower()
    assert "collatz" not in lowered
    assert "syracuse" not in lowered
    assert "3 * n + 1" not in text
    assert "v_2(3" not in text


def test_countdown_is_inapplicable_without_control_word():
    spec = CountdownSpec()
    attack = ControlObstructionAttack()
    assert attack.applicable(spec, AttackContext()) is False


def test_a_divisor_class_excludes_almost_all_length_one_exponents():
    spec = HiddenPowerClearDSpec()
    result = _obstruction(spec)
    family = next(
        item.evidence.get("family")
        for item in AttackPlanner().run(spec, spec.attack_context()).results
        if item.name == "control_word"
    )
    classification = length_one_divisor_class(int(family["base"]), int(family["p"]), int(family["r"]))
    assert classification["possible_k"] == (1,)
    certs = result.evidence.get("certificates") or ()
    class_div = [
        item
        for item in certs
        if item.get("scope") == "CLASS" and item.get("kind") == "divisibility"
    ]
    assert class_div
    assert all(item.get("status") in {"PROVED", "LEAN_CERTIFIED"} for item in class_div)
    assert result.status is AttackStatus.SUPPORTED
    assert result.scope is SearchScope.EXACT


def test_b_modular_class_on_finite_alphabet():
    spec = HiddenParityCarrySpec()
    result = _obstruction(spec)
    modular = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("kind") == "modular" and item.get("scope") == "CLASS"
    ]
    assert modular
    blocked = modular[0]["contradiction"].get("blocked_words") or ()
    allowed = modular[0]["contradiction"].get("allowed_words") or ()
    assert blocked
    assert allowed


def test_c_gcd_divisibility_class_can_be_empty():
    spec = HiddenOddPrimeClearSpec()
    result = _obstruction(spec)
    class_div = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("scope") == "CLASS" and item.get("kind") == "divisibility"
    ]
    assert class_div
    assert any(item.get("contradiction", {}).get("empty") for item in class_div)


def test_d_later_zero_is_a_domain_class():
    spec = HiddenPowerClearDSpec()
    result = _obstruction(spec)
    domain = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("kind") == "domain" and item.get("scope") == "CLASS"
    ]
    assert domain
    forbidden = domain[0]["contradiction"].get("forbidden_later_k") or ()
    assert 0 in tuple(forbidden)


def test_e_sign_candidate_outside_nonnegative_domain():
    spec = HiddenPositiveDoubleSpec()
    result = _obstruction(spec)
    signs = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("kind") == "sign"
    ]
    assert signs
    assert any(item.get("contradiction", {}).get("candidate") == -1 for item in signs)


def test_f_missing_sample_is_not_an_obstruction():
    spec = HiddenLargeFixedSpec()
    result = _obstruction(spec)
    certs = result.evidence.get("certificates") or ()
    class_empty = [
        item
        for item in certs
        if item.get("scope") == "CLASS" and item.get("contradiction", {}).get("empty")
    ]
    assert not class_empty
    impossible_family = [
        item
        for item in certs
        if item.get("scope") == "CLASS"
        and item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
        and item.get("kind") == "divisibility"
    ]
    assert not impossible_family


def test_named_attack_chains_control_word():
    spec = HiddenPowerClearDSpec()
    result = run_named_attack("control_obstruction", spec, spec.attack_context())
    assert result.name == "control_obstruction"
    assert result.evidence.get("certificates")


def test_planner_order_and_no_affine_injection():
    spec = HiddenPowerClearDSpec()
    context = spec.attack_context()
    assert context.affine is None
    report = AttackPlanner().run(spec, context)
    names = [item.name for item in report.results]
    assert names[3] == "control_word"
    assert names[4] == "control_obstruction"
    assert DEFAULT_ATTACK_ORDER.index("control_obstruction") == DEFAULT_ATTACK_ORDER.index(
        "control_word"
    ) + 1
    result = next(item for item in report.results if item.name == "control_obstruction")
    assert result.evidence.get("reconstructed_affine") is None
    assert spec.attack_context().affine is None


def test_lean_obstruction_has_no_sorry():
    path = Path(__file__).resolve().parents[3] / "formal" / "Problems" / "Engine" / "ControlObstruction.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert "exists_mul_eq_iff_dvd" in text
    assert "not_dvd_of_abs_gt" in text
    assert "cycle_constraint_dvd" in text
