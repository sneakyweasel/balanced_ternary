"""``F_{λ,U_m}`` as a ``ProblemSpec``. No SignedDigitEngine."""

from __future__ import annotations

from dataclasses import dataclass

from bt.transducers.mealy import minimize_mealy_count
from research.signed_digit_residual.discovery import (
    alphabet_m,
    reachable_from,
    signed_step,
)
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

INPUT_LENGTH = 8


@dataclass(frozen=True)
class SignedDigitResidualSpec:
    """LSD-first residual of bounded signed-digit normalization."""

    bound: int = 2
    gain: int = 1
    start_remaining: int = INPUT_LENGTH
    name: str = "signed_digit_residual"
    dimension: int = 1

    def __post_init__(self) -> None:
        if self.bound < 0:
            raise ValueError("bound must be nonnegative")
        if self.gain < 1:
            raise ValueError("gain must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if (self.bound, self.gain) != (2, 1) and self.name == "signed_digit_residual":
            object.__setattr__(self, "name", f"signed_digit_residual_g{self.gain}_m{self.bound}")

    @property
    def digits(self) -> tuple[int, ...]:
        return alphabet_m(self.bound)

    @property
    def candidate_region(self) -> frozenset[State]:
        reached = reachable_from(0, self.digits, self.gain)
        if reached is None:
            return frozenset()
        return frozenset((s,) for s in reached)

    @property
    def initial_state(self) -> State:
        return (0,)

    def emit(self, residual: int, control: int) -> tuple[int, int]:
        return signed_step(residual, control, self.gain)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        nxt, _out = self.emit(state[0], int(control))
        return (nxt,)

    def output(self, state: State, control: object) -> int:
        _nxt, out = self.emit(state[0], int(control))
        return out

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value > 0:
            return self.digits
        if state[0] == 0:
            return ()
        return (0,)

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
        return phase.value == 0 and state == (0,)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        target = state[0]
        found: set[State] = set()
        region = {s[0] for s in self.candidate_region}
        if not region:
            return ()
        for residual in region:
            for control in self.digits:
                nxt, _out = signed_step(residual, control, self.gain)
                if nxt == target:
                    found.add((residual,))
        return tuple(sorted(found))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", True)
        kwargs.setdefault("candidate_region", self.candidate_region)
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", tuple(sorted(self.candidate_region)))
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def signed_digit_spec(
    start_remaining: int = INPUT_LENGTH,
    bound: int = 2,
    gain: int = 1,
) -> SignedDigitResidualSpec:
    return SignedDigitResidualSpec(
        bound=bound,
        gain=gain,
        start_remaining=start_remaining,
    )


def raw_state_count(bound: int = 2, gain: int = 1) -> int:
    reached = reachable_from(0, alphabet_m(bound), gain)
    if reached is None:
        raise RuntimeError("reachable set exceeded the cap")
    return len(reached)


def minimized_state_count(bound: int = 2, gain: int = 1) -> int:
    digits = alphabet_m(bound)
    reached = reachable_from(0, digits, gain)
    if reached is None:
        raise RuntimeError("reachable set exceeded the cap")
    states = frozenset((s,) for s in reached)

    def mealy(state: State, control: object) -> tuple[State, int]:
        nxt, out = signed_step(state[0], int(control), gain)
        return (nxt,), out

    return minimize_mealy_count(states, digits, mealy)
