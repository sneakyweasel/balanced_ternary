"""Integer iterates of the map ``n ↦ n + W(n)``.

State is the integer ``n``. The adapter does not install monotonicity,
Hamming weight, a modulus, a Lyapunov, or an attractor.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.derivative import D, lsd
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

CONTROL = 0
DEFAULT_START = 4
BOX_BOUND = 2
INPUT_LENGTH = 8
INTEGER_STATE_CAP = 64


def digit_square_sum(n: int) -> int:
    """``W(n) = lsd(n)² + W(D(n))`` by exact local digits."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    total = 0
    current = n
    while current != 0:
        digit = int(lsd(current))
        total += digit * digit
        current = D(current)
    return total


def weight_drift(n: int) -> int:
    """``T(n) = n + W(n)``."""
    return n + digit_square_sum(n)


def interval_box(bound: int = BOX_BOUND) -> frozenset[State]:
    if isinstance(bound, bool) or not isinstance(bound, int) or bound < 0:
        raise ValueError(f"bound must be a nonnegative int, got {bound!r}")
    return frozenset((n,) for n in range(-bound, bound + 1))


@dataclass(frozen=True)
class WeightDriftSpec:
    """Integer dynamics of ``T(n)=n+W(n)`` with identity observation."""

    start: int = DEFAULT_START
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    box_bound: int = BOX_BOUND
    name: str = "balanced_ternary_weight_drift"
    dimension: int = 1

    def __post_init__(self) -> None:
        if isinstance(self.start, bool) or not isinstance(self.start, int):
            raise TypeError(f"start must be int, got {type(self.start).__name__}")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")
        if self.box_bound < 0:
            raise ValueError("box_bound must be nonnegative")

    @property
    def initial_state(self) -> State:
        return (self.start,)

    @property
    def candidate_region(self) -> frozenset[State]:
        return interval_box(self.box_bound)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return (weight_drift(state[0]),)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return int(state[0])

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value <= 0:
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
        nxt = weight_drift(self.start)
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("candidate_region", self.candidate_region)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("pair", (self.initial_state, (nxt,)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def weight_drift_spec(
    start_remaining: int = INPUT_LENGTH,
    start: int = DEFAULT_START,
) -> WeightDriftSpec:
    return WeightDriftSpec(start=start, start_remaining=start_remaining)
