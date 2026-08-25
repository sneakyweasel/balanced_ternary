"""Hint-free Euclidean remainder dynamics.

State is a pair of positive integers (a, b) with a > b > 0 at the seed.
The adapter exposes only (a, b) ↦ (b, a mod b). It does not install the
quotient q = ⌊a/b⌋ as a control, affine matrix, or observation.
"""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

CONTROL = 0
DEFAULT_A = 1071
DEFAULT_B = 462
INPUT_LENGTH = 24
INTEGER_STATE_CAP = 64


def require_positive_int(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    if n <= 0:
        raise ValueError(f"{name} must be a positive integer, got {n}")
    return n


def euclidean_step(state: State) -> State:
    a, b = int(state[0]), int(state[1])
    if b == 0:
        return (a, 0)
    return (b, a % b)


@dataclass(frozen=True)
class EuclideanSpec:
    """Two-dimensional remainder dynamics with dummy control."""

    a0: int = DEFAULT_A
    b0: int = DEFAULT_B
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    name: str = "euclidean_quotient"
    dimension: int = 2

    def __post_init__(self) -> None:
        require_positive_int(self.a0, "a0")
        require_positive_int(self.b0, "b0")
        if self.a0 <= self.b0:
            raise ValueError("seed must satisfy a0 > b0 > 0")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")

    @property
    def initial_state(self) -> State:
        return (self.a0, self.b0)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return euclidean_step(state)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> tuple[int, int]:
        del control, phase
        return (int(state[0]), int(state[1]))

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        if len(state) != 2:
            return ()
        b = state[1]
        if not isinstance(b, int) or isinstance(b, bool) or b == 0:
            return ()
        return (CONTROL,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        if self.is_accepting(state, phase):
            return True
        return phase.value > 0

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        if phase.value == 0:
            return True
        return len(state) == 2 and int(state[1]) == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]), int(state[1]))

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        nxt = euclidean_step(self.initial_state)
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1, 1)))
        kwargs.setdefault("pair", (self.initial_state, nxt))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def euclidean_spec(
    a0: int = DEFAULT_A,
    b0: int = DEFAULT_B,
    *,
    start_remaining: int = INPUT_LENGTH,
) -> EuclideanSpec:
    return EuclideanSpec(a0=a0, b0=b0, start_remaining=start_remaining)
