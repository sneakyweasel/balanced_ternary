"""Hint-free two-path integer map on Z^2. Scout material is not imported."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

CONTROL = 0
INPUT_LENGTH = 16
INTEGER_STATE_CAP = 32


def _require_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int, got {type(value).__name__}")
    return value


def next_state(state: tuple[int, int]) -> tuple[int, int] | None:
    x, y = state
    if y >= 1:
        return (x + y, y - 1)
    if x >= 1:
        return (x - 1, x + y)
    return None


@dataclass(frozen=True)
class TwoPathZ2Spec:
    """Singleton-control pair dynamics with coordinate observation."""

    start: tuple[int, int] = (3, 2)
    name: str = "two_path_z2"
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    dimension: int = 2

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "start",
            (_require_int(self.start[0], "x"), _require_int(self.start[1], "y")),
        )
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")

    @property
    def initial_state(self) -> State:
        return self.start

    def successors(self, state: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
        if len(state) != 2:
            return ()
        nxt = next_state((int(state[0]), int(state[1])))
        if nxt is None:
            return ()
        return (nxt,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        images = self.successors(tuple(int(part) for part in state))
        if len(images) != 1:
            raise ValueError(f"no unique successor at {state}")
        return images[0]

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> tuple[int, int]:
        del control, phase
        return (int(state[0]), int(state[1]))

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        window = tuple(int(part) for part in state)
        if window == (0, 0):
            return ()
        if not self.successors(window):
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
        if phase.value <= 0:
            return True
        return not self.successors(tuple(int(part) for part in state))

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del phase
        return tuple(int(part) for part in state) == (0, 0)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]), int(state[1]))

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        images = self.successors(self.start)
        nxt = images[0] if images else self.initial_state
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("pair", (self.initial_state, nxt))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def map_spec() -> TwoPathZ2Spec:
    return TwoPathZ2Spec()
