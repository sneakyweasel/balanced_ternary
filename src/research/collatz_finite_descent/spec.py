"""Shortcut Collatz as a ``ProblemSpec``.

State is the integer ``n``. The only legal control is its parity.
``AffineSystem`` is not used: the two branches have different rational
slopes, so modular/spectral attacks stay inapplicable.
"""

from __future__ import annotations

from dataclasses import dataclass

from research.collatz_finite_descent.shortcut import (
    CONTROL_EVEN,
    CONTROL_ODD,
    is_terminal,
    predecessors,
    require_positive_int,
    shortcut_step,
)
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

INTEGER_STATE_CAP = 16
REVERSE_DEPTH_CAP = 6
DEFAULT_START = 27


@dataclass(frozen=True)
class ShortcutSpec:
    """Integer shortcut dynamics with state-determined parity controls."""

    odd_mul: int = 3
    odd_add: int = 1
    start: int = DEFAULT_START
    start_remaining: int = 12
    state_cap: int = INTEGER_STATE_CAP
    reverse_max_depth: int = REVERSE_DEPTH_CAP
    name: str = "collatz_finite_descent"
    dimension: int = 1

    def __post_init__(self) -> None:
        require_positive_int(self.start, "start")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")
        if self.odd_mul != 3 or self.odd_add != 1:
            object.__setattr__(self, "name", f"collatz_finite_descent_{self.odd_mul}_{self.odd_add}")

    @property
    def initial_state(self) -> State:
        return (self.start,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        n = state[0]
        actual = CONTROL_EVEN if n % 2 == 0 else CONTROL_ODD
        if control != actual:
            raise ValueError(f"control {control!r} is not the parity of {n}")
        return (shortcut_step(n, self.odd_mul, self.odd_add),)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        n = state[0]
        if n <= 0:
            return ()
        return (CONTROL_EVEN if n % 2 == 0 else CONTROL_ODD,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del phase
        return is_terminal(state[0], self.odd_mul, self.odd_add)

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        return self.is_terminal(state, phase)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        return tuple((pred,) for pred in predecessors(state[0], self.odd_mul, self.odd_add))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault(
            "reverse_seeds",
            tuple(sorted((n,) for n in (1, 2))),
        )
        kwargs.setdefault("reverse_max_depth", self.reverse_max_depth)
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def shortcut_spec(
    start_remaining: int = 12,
    odd_mul: int = 3,
    odd_add: int = 1,
    start: int = DEFAULT_START,
) -> ShortcutSpec:
    return ShortcutSpec(
        odd_mul=odd_mul,
        odd_add=odd_add,
        start=start,
        start_remaining=start_remaining,
    )


def terminal_spec(start_remaining: int = 8) -> ShortcutSpec:
    """Forward dynamics from 1. Reachable set is the terminal cycle ``{1,2}``."""
    return ShortcutSpec(start=1, start_remaining=start_remaining, state_cap=256)
