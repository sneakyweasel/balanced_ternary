"""Discovered ``J₃`` residual of expanding ``T_λ`` as a ``ProblemSpec``.

State is the existing length-3 integer jet. ``T`` concatenates
``J₂(T_λ)`` with the second input digit and discards the third.
``I_d`` prepends a trit and drops the old third digit.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.transducers.mealy import mealy_partition, minimize_mealy_count
from research.balanced_ternary.expanding_j3 import (
    JET3_STATES,
    Jet3,
    j3_section,
    j3_transition,
    t_image,
)
from research.balanced_ternary.expanding_spec import I_CONTROLS, T_CONTROL
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

CONTROLS: tuple[object, ...] = I_CONTROLS + (T_CONTROL,)
JET3_REGION: frozenset[State] = frozenset(JET3_STATES)
INPUT_LENGTH = 8


def apply_control(jet: Jet3, control: object, gain: int = 1) -> Jet3:
    if control == T_CONTROL:
        return j3_transition(jet, gain)
    if isinstance(control, tuple) and len(control) == 2 and control[0] == "I":
        return j3_section(jet, control[1])
    raise ValueError(f"unknown expanding-J3 control {control!r}")


@dataclass(frozen=True)
class ExpandingJ3Spec:
    """Observational residual: current 3-digit integer jet of ``T_λ``."""

    gain: int = 1
    start_remaining: int = INPUT_LENGTH
    name: str = "expanding_j3"
    dimension: int = 3

    def __post_init__(self) -> None:
        if self.gain < 1:
            raise ValueError("gain must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.gain != 1 and self.name == "expanding_j3":
            object.__setattr__(self, "name", f"expanding_j3_gain_{self.gain}")

    @property
    def initial_state(self) -> State:
        return (0, 0, 0)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        return apply_control((state[0], state[1], state[2]), control, self.gain)

    def output(self, state: State, control: object) -> Jet3:
        return apply_control((state[0], state[1], state[2]), control, self.gain)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value > 0:
            return CONTROLS
        return ()

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
        return phase.value == 0 and state == (0, 0, 0)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]), int(state[1]), int(state[2]))

    def affine_system(self):
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        target = (state[0], state[1], state[2])
        found = {jet for jet in JET3_STATES if j3_transition(jet, self.gain) == target}
        return tuple(sorted(found))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", True)
        kwargs.setdefault("candidate_region", JET3_REGION)
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", tuple(sorted(JET3_REGION)))
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("functional", LinearFunctional((1, 0, 0)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def expanding_j3_spec(
    start_remaining: int = INPUT_LENGTH,
    gain: int = 1,
) -> ExpandingJ3Spec:
    return ExpandingJ3Spec(gain=gain, start_remaining=start_remaining)


def mealy_step(state: State, control: object, gain: int = 1) -> tuple[State, Jet3]:
    nxt = apply_control((state[0], state[1], state[2]), control, gain)
    return nxt, nxt


def raw_state_count(states: frozenset[State] = JET3_REGION) -> int:
    return len(states)


def image_state_count(gain: int = 1) -> int:
    return len(t_image(gain))


def current_output_count(states: frozenset[State] = JET3_REGION) -> int:
    return len(states)


def minimized_next_output_count(
    states: frozenset[State] = JET3_REGION,
    gain: int = 1,
) -> int:
    """Future-only Mealy classes if the emitted symbol is the next jet."""

    def step(state: State, control: object) -> tuple[State, Jet3]:
        return mealy_step(state, control, gain)

    return minimize_mealy_count(states, CONTROLS, step)


def mealy_classes(
    states: frozenset[State] = JET3_REGION,
    gain: int = 1,
) -> tuple[frozenset[State], ...]:
    def step(state: State, control: object) -> tuple[State, Jet3]:
        return mealy_step(state, control, gain)

    return mealy_partition(states, CONTROLS, step)
