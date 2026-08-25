"""No-repeat ``U_2`` product as a ``ProblemSpec``. Reuses ``signed_step``."""

from __future__ import annotations

from dataclasses import dataclass

from research.signed_digit_constrained_controls.discovery import (
    norepeat_automaton,
    product_reachable,
)
from research.signed_digit_residual.discovery import alphabet_m, signed_step
from research.signed_digit_residual.spec import SignedDigitResidualSpec
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

INPUT_LENGTH = 8


@dataclass(frozen=True)
class ConstrainedNoRepeatSpec:
    """Origin-reachable product of ``F_{1,U_2}`` with a no-repeat control automaton."""

    bound: int = 2
    gain: int = 1
    start_remaining: int = INPUT_LENGTH
    name: str = "signed_digit_constrained_controls"
    dimension: int = 2

    def __post_init__(self) -> None:
        if self.bound < 0:
            raise ValueError("bound must be nonnegative")
        if self.gain < 1:
            raise ValueError("gain must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")

    @property
    def digits(self) -> tuple[int, ...]:
        return alphabet_m(self.bound)

    @property
    def start_control(self) -> int:
        return self.bound + 1

    @property
    def automaton(self):
        return norepeat_automaton(self.digits, start=self.start_control)

    @property
    def candidate_region(self) -> frozenset[State]:
        reached = product_reachable(self.automaton, self.gain)
        if reached is None:
            return frozenset()
        return frozenset((int(residual), int(control)) for residual, control in reached)

    @property
    def initial_state(self) -> State:
        return (0, self.start_control)

    def emit(self, residual: int, control: int) -> tuple[int, int]:
        return signed_step(residual, control, self.gain)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        nxt, _out = self.emit(state[0], int(control))
        return (nxt, int(control))

    def output(self, state: State, control: object) -> int:
        _nxt, out = self.emit(state[0], int(control))
        return out

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del phase
        return self.automaton.legal(state[1])

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        if self.is_accepting(state, phase):
            return True
        if phase.value > 0:
            return True
        nxt, _out = self.emit(state[0], 0)
        return abs(nxt) < abs(state[0])

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        return phase.value == 0 and state[0] == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]), int(state[1]))

    def affine_system(self):
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        target_res, target_q = state
        found: set[State] = set()
        for src in self.candidate_region:
            for letter in self.automaton.legal(src[1]):
                nxt, _out = signed_step(src[0], int(letter), self.gain)
                if nxt == target_res and int(letter) == target_q:
                    found.add(src)
        return tuple(sorted(found))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", True)
        kwargs.setdefault("candidate_region", self.candidate_region)
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", tuple(sorted(self.candidate_region)))
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("functional", LinearFunctional((1, 0)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def constrained_spec(start_remaining: int = INPUT_LENGTH) -> ConstrainedNoRepeatSpec:
    return ConstrainedNoRepeatSpec(start_remaining=start_remaining)


__all__ = [
    "ConstrainedNoRepeatSpec",
    "SignedDigitResidualSpec",
    "constrained_spec",
]
