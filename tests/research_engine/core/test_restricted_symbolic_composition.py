"""Gated restricted symbolic-composition attack: exact rule, not a synthesizer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

from research_engine.attacks.restricted_symbolic_composition import (
    APPLICABLE,
    ENABLE_RESTRICTED_SYMBOLIC_COMPOSITION,
    FAMILY_NAME,
    GLOBAL_CONSEQUENCE_NONE,
    LEAN_THEOREM,
    MAP_MISMATCH,
    NOT_APPLICABLE,
    RULE_NAME,
    RestrictedSymbolicCompositionAttack,
    evaluate_odd_even_two_step,
    floor_power,
    odd_even_two_step,
)
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.control.baseline import load_v2_3_baseline, sha256_file, verify_manifest
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.planner.orchestrator import (
    DEFAULT_ATTACK_ORDER,
    DEFERRED_ATTACKS,
    EXPERIMENTAL_ATTACKS,
    AttackPlanner,
    run_named_attack,
)
from tests.research_engine.core.test_planner import CountdownSpec


@dataclass(frozen=True)
class FloorPowerToy:
    name: str = "floor_power_toy"
    dimension: int = 1
    initial_state: tuple[int, ...] = (13,)

    def successors(self, x: int) -> tuple[int, ...]:
        if x < 1:
            return ()
        if x % 2 == 0:
            return (isqrt(x),)
        return (isqrt(x * x * x),)


@dataclass(frozen=True)
class ReverseToy:
    name: str = "reverse_toy"
    dimension: int = 1
    initial_state: tuple[int, ...] = (1,)

    def successors(self, x: int) -> tuple[int, ...]:
        return (x + x,)


def _opt_in() -> AttackContext:
    return AttackContext(enable_restricted_symbolic_composition=True)


def test_gate_is_off_by_default():
    assert ENABLE_RESTRICTED_SYMBOLIC_COMPOSITION is False
    spec = FloorPowerToy()
    gated = RestrictedSymbolicCompositionAttack()
    assert gated.applicable(spec, AttackContext()) is False
    result = run_named_attack(FAMILY_NAME, spec, AttackContext())
    assert result.status is AttackStatus.INAPPLICABLE
    assert "gated" in result.claim


def test_odd_even_domain_and_composition():
    assert odd_even_two_step(3) is None
    assert floor_power(7) == 18
    assert odd_even_two_step(7) == 4
    spec = FloorPowerToy()
    payload = evaluate_odd_even_two_step(spec)
    assert payload.applicability == APPLICABLE
    assert payload.rule_name == RULE_NAME
    assert payload.depth == 2
    assert payload.candidate == "T^2(x) < x"
    assert payload.bounded_status == "SURVIVES"
    assert payload.exact_status == "VERIFIED"
    assert payload.lean_status == "PROVED"
    assert payload.lean_theorem.endswith(LEAN_THEOREM)
    assert payload.mathematical_status == "NEW_STRUCTURAL_LEMMA"
    assert payload.global_consequence == GLOBAL_CONSEQUENCE_NONE
    assert "TERMINATION" not in payload.global_consequence


def test_opt_in_recovers_juggler_rule():
    spec = FloorPowerToy()
    result = run_named_attack(FAMILY_NAME, spec, _opt_in())
    assert result.status is AttackStatus.SUPPORTED
    assert result.name == RULE_NAME
    assert result.kind is ClaimKind.REACHABLE
    assert result.scope is SearchScope.EXACT
    assert result.certificate_kind is CertificateKind.EXACT_ARITHMETIC_IDENTITY
    assert result.evidence["lean_status"] == "PROVED"
    assert result.evidence["global_consequence"] == GLOBAL_CONSEQUENCE_NONE
    assert result.evidence["applicability"] == APPLICABLE
    assert LEAN_THEOREM in result.certificates[0]


def test_negative_map_is_not_applicable():
    payload = evaluate_odd_even_two_step(ReverseToy())
    assert payload.applicability == NOT_APPLICABLE
    assert payload.failure_reason == MAP_MISMATCH
    result = run_named_attack(FAMILY_NAME, ReverseToy(), _opt_in())
    assert result.status is AttackStatus.INAPPLICABLE
    assert result.evidence["failure_reason"] == MAP_MISMATCH
    assert result.evidence["global_consequence"] == GLOBAL_CONSEQUENCE_NONE


def test_no_successor_is_not_supported_composition():
    payload = evaluate_odd_even_two_step(CountdownSpec())
    assert payload.applicability == NOT_APPLICABLE
    assert payload.failure_reason == "NO_SUPPORTED_COMPOSITION"


def test_planner_does_not_execute_experimental_attack():
    report = AttackPlanner().run(CountdownSpec(), AttackContext(live_only=True))
    names = [item.name for item in report.results]
    assert FAMILY_NAME not in names
    assert RULE_NAME not in names
    assert FAMILY_NAME not in DEFAULT_ATTACK_ORDER
    assert RULE_NAME not in DEFAULT_ATTACK_ORDER
    assert EXPERIMENTAL_ATTACKS.isdisjoint(DEFAULT_ATTACK_ORDER)
    assert DEFERRED_ATTACKS == ("symbolic",)


def test_cannot_silently_claim_termination_or_enlarge_depth():
    payload = evaluate_odd_even_two_step(FloorPowerToy())
    assert payload.depth == 2
    assert payload.global_consequence == GLOBAL_CONSEQUENCE_NONE
    assert payload.mathematical_status != "TERMINATION_PROVED"
    assert payload.mathematical_status != "GLOBAL_RANKING"
    result = run_named_attack("odd_even_two_step_decrease", FloorPowerToy(), _opt_in())
    assert result.evidence["depth"] == 2
    assert result.evidence["global_consequence"] == GLOBAL_CONSEQUENCE_NONE


def test_frozen_v23_seeds_untouched():
    baseline = load_v2_3_baseline()
    recorded = verify_manifest(baseline.manifest)
    assert recorded["files"]["historical.json"] == sha256_file(SEED_PATH)
    assert recorded["files"]["target_board.json"] == sha256_file(BOARD_PATH)
    assert recorded["default_attack_order"] == list(DEFAULT_ATTACK_ORDER)
    assert recorded["deferred_attacks"] == list(DEFERRED_ATTACKS)
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
