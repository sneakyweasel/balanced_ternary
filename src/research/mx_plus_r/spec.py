"""Hint-free accelerated (mx+r) dynamics.

State is a positive odd integer. The adapter exposes only the exact
transition. It does not install a valuation, affine family, branch
predicate, cycle equation, or modular restriction.
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


def require_odd_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int, got {type(value).__name__}")
    if value % 2 == 0:
        raise ValueError(f"{name} must be odd, got {value}")
    return value


def require_positive_odd(n: int, name: str = "n") -> int:
    n = require_odd_int(n, name)
    if n <= 0:
        raise ValueError(f"{name} must be a positive odd integer, got {n}")
    return n


def mx_plus_r_step(n: int, m: int, r: int) -> int:
    """``T(n) = (m n + r)`` divided by 2 until the result is odd."""
    n = require_positive_odd(n)
    y = m * n + r
    if y == 0:
        raise ValueError(f"m n + r vanished at n={n}")
    while y % 2 == 0:
        y //= 2
    if y <= 0:
        raise ValueError(f"T_{m},{r}({n}) is not a positive odd integer, got {y}")
    return y


def spec_name(m: int, r: int) -> str:
    return f"mx_plus_r_{m}_{r}"


@dataclass(frozen=True)
class MxPlusRSpec:
    """Odd-only integer dynamics with identity observation and dummy control."""

    m: int
    r: int
    start: int = DEFAULT_START
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    name: str = ""
    dimension: int = 1

    def __post_init__(self) -> None:
        require_odd_int(self.m, "m")
        require_odd_int(self.r, "r")
        require_positive_odd(self.start, "start")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")
        if not self.name:
            object.__setattr__(self, "name", spec_name(self.m, self.r))

    @property
    def initial_state(self) -> State:
        return (self.start,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return (mx_plus_r_step(state[0], self.m, self.r),)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return int(state[0])

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        n = state[0]
        if not isinstance(n, int) or isinstance(n, bool) or n <= 0 or n % 2 == 0:
            return ()
        y = self.m * n + self.r
        if y == 0:
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
        nxt = mx_plus_r_step(self.start, self.m, self.r)
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("pair", (self.initial_state, (nxt,)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def mx_plus_r_spec(
    m: int,
    r: int,
    *,
    start_remaining: int = INPUT_LENGTH,
    start: int = DEFAULT_START,
) -> MxPlusRSpec:
    return MxPlusRSpec(m=m, r=r, start=start, start_remaining=start_remaining)
