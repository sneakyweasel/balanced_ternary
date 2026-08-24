"""Planner cannot promote a bounded census to live infinitude."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.affine_system import AffineSystem
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus
from research_engine.planner.ledger import LedgerError, ResearchLedger
from research_engine.planner.negative import ForbiddenImplication, NegativeKnowledge
from research_engine.planner.orchestrator import AttackPlanner, promote_if_legal


@dataclass(frozen=True)
class CountdownSpec:
    name: str = "countdown_toy"
    dimension: int = 1
    initial_state: tuple[int, ...] = (0,)
    start_remaining: int = 2

    def transition(self, state: tuple[int, ...], control: int, phase: IntPhase) -> tuple[int, ...]:
        del phase
        return (state[0] + control,)

    def legal_controls(self, state: tuple[int, ...], phase: IntPhase) -> tuple[int, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (-1, 0, 1)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return IntPhase(phase.value - 1)

    def is_terminal(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        del state
        return True

    def is_accepting(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        return phase.value == 0 and state[0] == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(state)


def test_negative_knowledge_blocks_terminal_to_live():
    knowledge = NegativeKnowledge()
    blocked = knowledge.forbids("terminal_unbounded", "live_unbounded")
    assert blocked is not None
    assert knowledge.forbids_kinds(ClaimKind.LIVE_SLICE, ClaimKind.LIVE) is not None
    assert knowledge.forbids_kinds(ClaimKind.CO_REACHABLE, ClaimKind.LIVE) is not None
    assert knowledge.forbids_kinds(ClaimKind.LIVE, ClaimKind.LIVE) is None


def test_planner_records_bounded_census_not_live_infinitude():
    ledger = ResearchLedger()
    ledger.add_hypothesis(
        Hypothesis(
            id="live_infinite",
            statement="the live set is infinite",
            kind=ClaimKind.LIVE,
            intended_scope=SearchScope.EXACT,
            status=HypothesisStatus.OPEN,
        )
    )
    report = AttackPlanner(ledger).run(
        CountdownSpec(),
        AttackContext(
            live_only=True,
            affine=AffineSystem(A=((3,),), translations={0: (0,)}),
            functional=LinearFunctional((1,)),
        ),
    )
    names = [item.name for item in report.results]
    assert names[0] == "reconnaissance"
    assert "modular" in names
    skipped = {item.attack: item.reason for item in report.skipped}
    assert skipped["affine"].startswith("inapplicable")
    assert skipped["spectral"] == "not implemented in this phase"
    census = ledger.get("countdown_toy_live_slice_census")
    assert census.kind == ClaimKind.LIVE_SLICE
    assert census.intended_scope == SearchScope.BOUNDED
    assert ledger.get("live_infinite").status is HypothesisStatus.OPEN
    recon = report.results[0]
    with pytest.raises(LedgerError):
        promote_if_legal(ledger, "live_infinite", recon)
    assert ledger.get("live_infinite").status is HypothesisStatus.OPEN
    assert any(jump.to_kind is ClaimKind.LIVE for jump in report.blocked_jumps)


def test_closed_attack_is_skipped():
    extra = ForbiddenImplication(
        id="skip_functional",
        antecedent="functional_sample_bound",
        consequent="functional_invariant",
        from_kind=ClaimKind.LIVE_SLICE,
        to_kind=ClaimKind.LIVE,
        statement="skip functional",
        counterexample="test",
        closed_attacks=("functional",),
    )
    ledger = ResearchLedger(knowledge=NegativeKnowledge().extend((extra,)))
    report = AttackPlanner(ledger).run(
        CountdownSpec(),
        AttackContext(functional=LinearFunctional((1,))),
    )
    assert all(item.name != "functional" for item in report.results)
    assert any(item.attack == "functional" and "closed" in item.reason for item in report.skipped)


def test_park_and_refute_do_not_require_matching_attack():
    ledger = ResearchLedger()
    ledger.add_hypothesis(
        Hypothesis(
            id="live_infinite",
            statement="the live set is infinite",
            kind=ClaimKind.LIVE,
            intended_scope=SearchScope.EXACT,
        )
    )
    parked = ledger.decide("live_infinite", DecisionKind.PARK, "no family, no contraction")
    assert parked.status is HypothesisStatus.PARKED
    ledger.add_hypothesis(
        Hypothesis(
            id="slice_nonincreasing",
            statement="|x| is nonincreasing on the start layer",
            kind=ClaimKind.LIVE_SLICE,
            intended_scope=SearchScope.BOUNDED,
        )
    )
    report = AttackPlanner(ledger).run(
        CountdownSpec(),
        AttackContext(functional=LinearFunctional((1,))),
    )
    functional = next(item for item in report.results if item.name == "functional")
    updated = ledger.decide(
        "slice_nonincreasing",
        DecisionKind.REFUTE,
        functional.claim,
        from_result=functional,
    )
    assert updated.status is HypothesisStatus.REFUTED
    assert ledger.get("live_infinite").status is HypothesisStatus.PARKED
