"""Integer iterates of the accelerated odd-only map.

State is a positive odd integer. The adapter does not install valuation,
parity, a cycle, a Lyapunov, or a residue class as an observation.
"""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

CONTROL = 0
DEFAULT_START = 27
INPUT_LENGTH = 12
INTEGER_STATE_CAP = 16


def require_positive_odd(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    if n <= 0 or n % 2 == 0:
        raise ValueError(f"{name} must be a positive odd integer, got {n}")
    return n


def syracuse_step(n: int) -> int:
    """``S(n) = (3n+1)`` divided by 2 until the result is odd."""
    n = require_positive_odd(n)
    y = 3 * n + 1
    while y % 2 == 0:
        y //= 2
    return y


@dataclass(frozen=True)
class SyracuseSpec:
    """Odd-only integer dynamics with identity observation and dummy control."""

    start: int = DEFAULT_START
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    name: str = "syracuse"
    dimension: int = 1

    def __post_init__(self) -> None:
        require_positive_odd(self.start, "start")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")

    @property
    def initial_state(self) -> State:
        return (self.start,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return (syracuse_step(state[0]),)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return int(state[0])

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        n = state[0]
        if not isinstance(n, int) or isinstance(n, bool) or n <= 0 or n % 2 == 0:
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
        nxt = syracuse_step(self.start)
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("pair", (self.initial_state, (nxt,)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def syracuse_spec(
    start_remaining: int = INPUT_LENGTH,
    start: int = DEFAULT_START,
) -> SyracuseSpec:
    return SyracuseSpec(start=start, start_remaining=start_remaining)
