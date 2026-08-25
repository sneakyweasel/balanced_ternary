"""Hint-free companion-window integer maps with first-coordinate sign.

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
    return CENSUS_CUBE_SIDE**dimension


def skip_attacks_for_dimension(dimension: int) -> tuple[str, ...]:
    if census_cells(dimension) > MAX_CENSUS_CELLS:
        return ("vector_affine", "matrix_word_invariant")
    return ()


@dataclass(frozen=True)
class CompanionObsSpec:
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
            object.__setattr__(self, "name", f"companion_obs_d{len(win)}")

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
        if observation(window) < 0:
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
        return observation(tuple(int(part) for part in state)) < 0

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


def nonneg_small_spec() -> CompanionObsSpec:
    return CompanionObsSpec(
        name="companion_obs_nonneg_small",
        last_row=(1, 1),
        window=(1, 1),
    )


def early_negative_spec() -> CompanionObsSpec:
    return CompanionObsSpec(
        name="companion_obs_early_negative",
        last_row=(1, 1),
        window=(2, -1),
    )


def periodic_sign_spec() -> CompanionObsSpec:
    return CompanionObsSpec(
        name="companion_obs_periodic_sign",
        last_row=(-1, 0),
        window=(1, 1),
    )


def finite_negative_spec() -> CompanionObsSpec:
    return CompanionObsSpec(
        name="companion_obs_finite_negative",
        last_row=(1, 1),
        window=(5, -3),
    )


def order3_spec() -> CompanionObsSpec:
    return CompanionObsSpec(
        name="companion_obs_order3",
        last_row=(30, -31, 10),
        window=(3, 10, 38),
    )


def order10_spec() -> CompanionObsSpec:
    return CompanionObsSpec(
        name="companion_obs_order10",
        last_row=(
            -41423825675781250,
            20682499470546875,
            13815580471875,
            856834394000,
            -205750047100,
            55996590,
            -2333386,
            749576,
            -378,
            -1,
        ),
        window=(
            35,
            574,
            34592,
            8999992,
            115734548,
            5682747424,
            1837938758372,
            13061285121472,
            397924220049188,
            290333397927490624,
        ),
    )


def map_spec() -> CompanionObsSpec:
    return order10_spec()


CATALOG: dict[str, CompanionObsSpec] = {
    spec.name: spec
    for spec in (
        nonneg_small_spec(),
        early_negative_spec(),
        periodic_sign_spec(),
        finite_negative_spec(),
        order3_spec(),
        order10_spec(),
    )
}
