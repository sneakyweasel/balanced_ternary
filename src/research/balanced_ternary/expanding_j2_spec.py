"""Discovered ``J₂`` residual of expanding ``T_λ`` as a ``ProblemSpec``.

State is the existing length-2 integer jet ``(lsd, lsd∘D)``. Section
``I_c`` prepends a trit; ``T`` applies the exact jet map, which depends
only on the first digit. Mixed ``I``/``T`` steps are not one ``Ax+b``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.transducers.mealy import mealy_partition, minimize_mealy_count
from research.balanced_ternary.expanding_j2 import (
    JET2_STATES,
    Jet2,
    j2_section,
    j2_transition,
    t_image,
)
from research.balanced_ternary.expanding_spec import I_CONTROLS, T_CONTROL
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

CONTROLS: tuple[object, ...] = I_CONTROLS + (T_CONTROL,)
JET2_REGION: frozenset[State] = frozenset(JET2_STATES)
INPUT_LENGTH = 8


def apply_control(jet: Jet2, control: object, gain: int = 1) -> Jet2:
    if control == T_CONTROL:
        return j2_transition(jet, gain)
    if isinstance(control, tuple) and len(control) == 2 and control[0] == "I":
        return j2_section(jet, control[1])
    raise ValueError(f"unknown expanding-J2 control {control!r}")


@dataclass(frozen=True)
class ExpandingJ2Spec:
    """Observational residual: current 2-digit integer jet of ``T_λ``."""

    gain: int = 1
    start_remaining: int = INPUT_LENGTH
    name: str = "expanding_j2"
    dimension: int = 2

    def __post_init__(self) -> None:
        if self.gain < 1:
            raise ValueError("gain must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.gain != 1 and self.name == "expanding_j2":
            object.__setattr__(self, "name", f"expanding_j2_gain_{self.gain}")

    @property
    def initial_state(self) -> State:
        return (0, 0)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        return apply_control((state[0], state[1]), control, self.gain)

    def output(self, state: State, control: object) -> Jet2:
        return apply_control((state[0], state[1]), control, self.gain)

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
        return phase.value == 0 and state == (0, 0)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]), int(state[1]))

    def affine_system(self):
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        target = (state[0], state[1])
        found = {jet for jet in JET2_STATES if j2_transition(jet, self.gain) == target}
        return tuple(sorted(found))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", True)
        kwargs.setdefault("candidate_region", JET2_REGION)
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", tuple(sorted(JET2_REGION)))
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("functional", LinearFunctional((1, 0)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def expanding_j2_spec(
    start_remaining: int = INPUT_LENGTH,
    gain: int = 1,
) -> ExpandingJ2Spec:
    return ExpandingJ2Spec(gain=gain, start_remaining=start_remaining)


def mealy_step(state: State, control: object, gain: int = 1) -> tuple[State, Jet2]:
    nxt = apply_control((state[0], state[1]), control, gain)
    return nxt, nxt


def raw_state_count(states: frozenset[State] = JET2_REGION) -> int:
    return len(states)


def image_state_count(gain: int = 1) -> int:
    return len(t_image(gain))


def current_output_count(states: frozenset[State] = JET2_REGION) -> int:
    """Full-sequence classes: the current ``J₂`` is the state."""
    return len(states)


def minimized_next_output_count(
    states: frozenset[State] = JET2_REGION,
    gain: int = 1,
) -> int:
    """Future-only Mealy classes if the emitted symbol is the next jet."""

    def step(state: State, control: object) -> tuple[State, Jet2]:
        return mealy_step(state, control, gain)

    return minimize_mealy_count(states, CONTROLS, step)


def mealy_classes(
    states: frozenset[State] = JET2_REGION,
    gain: int = 1,
) -> tuple[frozenset[State], ...]:
    def step(state: State, control: object) -> tuple[State, Jet2]:
        return mealy_step(state, control, gain)

    return mealy_partition(states, CONTROLS, step)
