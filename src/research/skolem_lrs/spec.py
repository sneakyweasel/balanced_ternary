"""Hint-free companion-window integer maps.

State is a fixed-length integer window. The successor is the exact
shift that appends one linear combination of the window. Dummy control.
No affine-system hint. Observation is the first coordinate.
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
MAX_ABS_BITS = 512
# Frozen vector census materializes a cube of side 25. Skip that attack
# when the cube exceeds this cell budget (adapter bound, not a new attack).
CENSUS_CUBE_SIDE = 25
MAX_CENSUS_CELLS = 50_000


def _require_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int, got {type(value).__name__}")
    return value


def _require_int_tuple(values: tuple[int, ...], name: str) -> tuple[int, ...]:
    if not values:
        raise ValueError(f"{name} must be nonempty")
    return tuple(_require_int(item, name) for item in values)


def next_window(window: tuple[int, ...], last_row: tuple[int, ...]) -> tuple[int, ...]:
    if len(window) != len(last_row):
        raise ValueError("window and last_row must have equal length")
    nxt = sum(coeff * value for coeff, value in zip(last_row, window, strict=True))
    return window[1:] + (nxt,)


def observation(window: tuple[int, ...]) -> int:
    return int(window[0])


def over_budget(window: tuple[int, ...]) -> bool:
    return any(int(part).bit_length() > MAX_ABS_BITS for part in window)


def census_cells(dimension: int) -> int:
    return CENSUS_CUBE_SIDE ** dimension


def skip_attacks_for_dimension(dimension: int) -> tuple[str, ...]:
    if census_cells(dimension) > MAX_CENSUS_CELLS:
        return ("vector_affine", "matrix_word_invariant")
    return ()


@dataclass(frozen=True)
class CompanionShiftSpec:
    """Fixed-length window dynamics with dummy control and first-coordinate output."""

    last_row: tuple[int, ...]
    window: tuple[int, ...]
    name: str = ""
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    dimension: int = 0

    def __post_init__(self) -> None:
        last = _require_int_tuple(self.last_row, "last_row")
        win = _require_int_tuple(self.window, "window")
        if len(last) != len(win):
            raise ValueError("last_row and window must have equal length")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")
        object.__setattr__(self, "last_row", last)
        object.__setattr__(self, "window", win)
        object.__setattr__(self, "dimension", len(win))
        if not self.name:
            object.__setattr__(self, "name", f"companion_shift_d{len(win)}")

    def successors(self, state: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
        if len(state) != self.dimension:
            return ()
        if over_budget(state):
            return ()
        return (next_window(state, self.last_row),)

    @property
    def initial_state(self) -> State:
        return self.window

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        images = self.successors(tuple(int(part) for part in state))
        if len(images) != 1:
            raise ValueError(f"no unique successor at {state}")
        return images[0]

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return observation(tuple(int(part) for part in state))

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        window = tuple(int(part) for part in state)
        if observation(window) == 0:
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
        return phase.value <= 0 or over_budget(tuple(int(part) for part in state))

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del phase
        return observation(tuple(int(part) for part in state)) == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return tuple(int(part) for part in state)

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        images = self.successors(self.window)
        nxt = images[0] if images else self.initial_state
        coeffs = (1,) + tuple(0 for _ in range(self.dimension - 1))
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional(coeffs))
        kwargs.setdefault("pair", (self.initial_state, nxt))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        kwargs.setdefault("skip_attacks", skip_attacks_for_dimension(self.dimension))
        return AttackContext(**kwargs)


def zero_small_spec() -> CompanionShiftSpec:
    return CompanionShiftSpec(
        name="companion_shift_zero_small",
        last_row=(-2, 3),
        window=(-7, -6),
    )


def positive_spec() -> CompanionShiftSpec:
    return CompanionShiftSpec(
        name="companion_shift_positive",
        last_row=(1, 1),
        window=(1, 1),
    )


def periodic_spec() -> CompanionShiftSpec:
    return CompanionShiftSpec(
        name="companion_shift_periodic",
        last_row=(-1, 0),
        window=(1, 0),
    )


def order3_spec() -> CompanionShiftSpec:
    return CompanionShiftSpec(
        name="companion_shift_order3",
        last_row=(30, -31, 10),
        window=(3, 10, 38),
    )


def order6_spec() -> CompanionShiftSpec:
    return CompanionShiftSpec(
        name="companion_shift_order6",
        last_row=(-4225, 8970, -5267, 532, -19, 10),
        window=(12, 49, 374, 6003, 21520, 150773),
    )


def map_spec() -> CompanionShiftSpec:
    return order6_spec()


CATALOG: dict[str, CompanionShiftSpec] = {
    spec.name: spec
    for spec in (
        zero_small_spec(),
        positive_spec(),
        periodic_spec(),
        order3_spec(),
        order6_spec(),
    )
}
