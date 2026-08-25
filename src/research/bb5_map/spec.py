"""Hint-free one-variable partial integer map.

Exposes only the exact successor relation and identity observation.
No literature names, residue labels, or affine-system hint.
"""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.algebra.linear_functionals import LinearFunctional
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


def map_images(n: int) -> tuple[int, ...]:
    """Integers y with 3y = 5n + 18 or 3y = 5n + 22, on n >= 0."""
    n = _require_int(n, "n")
    if n < 0:
        return ()
    found: list[int] = []
    for offset in (18, 22):
        total = 5 * n + offset
        if total % 3 == 0:
            found.append(total // 3)
    return tuple(found)


@dataclass(frozen=True)
class PartialFiveThreeSpec:
    """One-variable integer dynamics with identity observation and dummy control."""

    name: str = "partial_five_three"
    start: int = 0
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    dimension: int = 1

    def __post_init__(self) -> None:
        _require_int(self.start, "start")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")
        if not self.name:
            raise ValueError("name must be nonempty")

    def successors(self, x: int) -> tuple[int, ...]:
        return map_images(x)

    @property
    def initial_state(self) -> State:
        return (self.start,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        images = self.successors(int(state[0]))
        if len(images) != 1:
            raise ValueError(f"no unique successor at {state}")
        return (images[0],)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return int(state[0])

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        if len(self.successors(int(state[0]))) != 1:
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
        del state
        return phase.value == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        images = self.successors(self.start)
        nxt = (images[0],) if len(images) == 1 else self.initial_state
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("pair", (self.initial_state, nxt))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def map_spec(*, start: int = 0) -> PartialFiveThreeSpec:
    return PartialFiveThreeSpec(start=start)
