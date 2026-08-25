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
        if item.get("scope") == "CLASS"
        and item.get("kind") == "divisibility"
        and item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
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
    assert "last_step_remainder" in text
    assert "cycle_abs_obstruction" in text
    assert "two_step_remainder" in text
    assert "two_step_elimination" in text
    assert "dvd_constant_of_dvd_remainder" in text


def _symbolic_certs(result) -> list[dict]:
    return [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("scope") == "SYMBOLIC_CLASS"
        and item.get("status") in {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}
    ]


def test_symbolic_a_infinite_last_k_class_on_power_clear():
    spec = HiddenPowerClearDSpec()
    result = _obstruction(spec)
    symbolic = [
        item
        for item in _symbolic_certs(result)
        if item.get("kind") == "bound" and item.get("summary", {}).get("length") == 2
    ]
    assert symbolic
    k_min = symbolic[0]["summary"]["k_min"]
    assert k_min >= 2
    assert symbolic[0]["contradiction"].get("empty_in_class") is True
    assert result.evidence.get("symbolic") is True
    assert result.status is AttackStatus.SUPPORTED


def test_symbolic_b_finite_exceptions_are_outside_the_class():
    spec = HiddenPowerClearDSpec()
    result = _obstruction(spec)
    refuted_total = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("scope") == "CLASS"
        and item.get("status") == "REFUTED"
        and item.get("constraint", {}).get("form") == "all words"
        and item.get("summary", {}).get("length") == 2
    ]
    assert refuted_total
    exceptions = {tuple(word) for word in refuted_total[0]["contradiction"].get("exceptions") or ()}
    assert (1, 1) in exceptions
    symbolic = [
        item
        for item in _symbolic_certs(result)
        if item.get("kind") == "bound" and item.get("summary", {}).get("length") == 2
    ]
    k_min = symbolic[0]["summary"]["k_min"]
    assert all(word[-1] < k_min for word in exceptions)


def test_symbolic_c_length_parity_on_sign_clear():
    from research_engine.benchmarks.hidden_piecewise import HiddenOneMinusClearSpec

    spec = HiddenOneMinusClearSpec()
    result = _obstruction(spec)
    odd = length_one_divisor_class(2, -1, 1)
    assert odd["empty"] is True
    class_div = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("scope") == "CLASS"
        and item.get("kind") == "divisibility"
        and item.get("contradiction", {}).get("empty")
    ]
    assert class_div
    even_symbolic = [
        item
        for item in _symbolic_certs(result)
        if item.get("kind") == "bound" and item.get("summary", {}).get("length") == 2
    ]
    assert even_symbolic
    exceptions = even_symbolic[0]["contradiction"].get("exceptions_outside_class") or ()
    assert any(tuple(word) == (0, 0) for word in exceptions)


def test_symbolic_d_discovers_last_control_summary():
    spec = HiddenPowerClearDSpec()
    result = _obstruction(spec)
    summaries = [
        item.get("summary") or {}
        for item in _symbolic_certs(result)
        if item.get("contradiction", {}).get("remainder_independent_of_last")
    ]
    assert summaries
    assert summaries[0].get("remainder_independent_of_last") is True
    assert summaries[0].get("exact_relation")
    assert summaries[0].get("divisibility_mode") == "SYMBOLIC_DIVISIBILITY"


def test_symbolic_e_does_not_silently_weaken_total_impossibility():
    spec = HiddenPowerClearDSpec()
    result = _obstruction(spec)
    refuted = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("status") == "REFUTED" and item.get("constraint", {}).get("form") == "all words"
    ]
    assert refuted
    proved_all = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("scope") in {"CLASS", "SYMBOLIC_CLASS"}
        and item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
        and item.get("constraint", {}).get("form") == "all words"
    ]
    assert not proved_all


def test_symbolic_f_zero_remainder_is_not_an_obstruction():
    from research_engine.benchmarks.hidden_piecewise import HiddenOddPartSpec

    spec = HiddenOddPartSpec()
    result = _obstruction(spec)
    symbolic_bound = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("scope") == "SYMBOLIC_CLASS"
        and item.get("kind") == "bound"
        and item.get("status") in {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}
    ]
    assert not symbolic_bound
    empty_class = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("scope") in {"CLASS", "SYMBOLIC_CLASS"}
        and item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
        and item.get("contradiction", {}).get("empty")
    ]
    assert not empty_class


def test_last_k_threshold_is_symbolic_not_enumerative():
    from research_engine.attacks.control_obstruction import last_k_threshold

    assert last_k_threshold(2, 1, 1, 2) == 2
    assert last_k_threshold(2, 3, 1, 2) == 4
    assert last_k_threshold(2, 1, 0, 2) is None


def _recursive_certs(result, kind=None):
    items = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("scope") == "RECURSIVE_INVARIANT"
    ]
    if kind is None:
        return items
    return [item for item in items if item.get("kind") == kind]


def test_recursive_a_residue_when_magnitude_inapplicable():
    spec = HiddenOddPrimeClearSpec()
    result = _obstruction(spec)
    modular = [
        item
        for item in _recursive_certs(result, "modular")
        if item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
        and item.get("contradiction", {}).get("magnitude_obstruction") == "INAPPLICABLE"
    ]
    assert modular
    assert result.evidence.get("recursive") is True


def test_recursive_b_gcd_bound_is_infinite():
    spec = HiddenOddPrimeClearSpec()
    result = _obstruction(spec)
    gcd_certs = [
        item
        for item in _recursive_certs(result, "gcd")
        if item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
        and item.get("summary", {}).get("infinite")
    ]
    assert gcd_certs
    assert gcd_certs[0]["contradiction"].get("gcd_bound") == 2


def test_recursive_c_odd_prime_valuation():
    from research_engine.benchmarks.hidden_piecewise import HiddenFiveClearSpec

    spec = HiddenFiveClearSpec()
    result = _obstruction(spec)
    valuation = [
        item
        for item in _recursive_certs(result, "valuation")
        if item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
    ]
    assert valuation
    prime = valuation[0]["contradiction"].get("prime")
    assert prime is not None and prime % 2 == 1
    assert valuation[0]["contradiction"].get("magnitude_obstruction") == "INAPPLICABLE"


def test_recursive_d_finite_exceptions_are_recorded():
    spec = HiddenOddPrimeClearSpec()
    result = _obstruction(spec)
    div = [
        item
        for item in _recursive_certs(result, "divisibility")
        if item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
    ]
    assert div
    exceptions = {tuple(word) for word in div[0]["contradiction"].get("exceptions") or ()}
    assert (1, 0) in exceptions
    total = [
        item
        for item in result.evidence.get("certificates") or ()
        if item.get("constraint", {}).get("form") == "all words"
        and item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
    ]
    assert not total


def test_recursive_e_false_seed_residue_is_refuted():
    spec = HiddenOddPrimeClearSpec()
    result = _obstruction(spec)
    refuted = [
        item
        for item in _recursive_certs(result, "invariant")
        if item.get("status") == "REFUTED"
    ]
    assert refuted


def test_recursive_f_mixed_predicates():
    from research_engine.benchmarks.hidden_piecewise import HiddenFiveClearSpec

    spec = HiddenFiveClearSpec()
    result = _obstruction(spec)
    proved = [
        item
        for item in _recursive_certs(result)
        if item.get("status") in {"PROVED", "LEAN_CERTIFIED"}
    ]
    kinds = {item.get("kind") for item in proved}
    assert "divisibility" in kinds
    assert "gcd" in kinds or "modular" in kinds
    assert "valuation" in kinds
    assert all(
        item.get("contradiction", {}).get("magnitude_obstruction") == "INAPPLICABLE"
        or item.get("summary", {}).get("magnitude") == "INAPPLICABLE"
        for item in proved
    )


def test_recursive_identity_is_discovered_not_seeded():
    from research_engine.attacks.control_obstruction import (
        elimination_constant,
        elimination_identity_holds,
    )

    assert elimination_constant(3, 1, 1, 0) == 2
    assert elimination_identity_holds(3, 1, 1, 4, 0)
    assert elimination_identity_holds(5, 1, 1, 3, 0)
