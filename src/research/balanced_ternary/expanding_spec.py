"""Discovered LSD residual of expanding ``T_λ`` as a ``ProblemSpec``.

State is the current LSD. Section controls ``I_a`` set that LSD; the
``T`` control applies the exact residue map ``r ↦ lsd(-λ r)``. The
integer ``n`` is not a state. Mixed ``I``/``T`` steps are not one
``Ax+b``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.transducers.mealy import mealy_partition, minimize_mealy_count
from research.balanced_ternary.expanding_d import TRITS, expanding_d, residue_step
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

I_CONTROLS: tuple[tuple[str, int], ...] = (("I", -1), ("I", 0), ("I", 1))
T_CONTROL: tuple[str] = ("T",)
CONTROLS: tuple[object, ...] = I_CONTROLS + (T_CONTROL,)
RESIDUES: frozenset[State] = frozenset({(-1,), (0,), (1,)})
INPUT_LENGTH = 8


def apply_control(residue: int, control: object, gain: int = 1) -> int:
    if control == T_CONTROL:
        return residue_step(residue, gain)
    if isinstance(control, tuple) and len(control) == 2 and control[0] == "I":
        digit = control[1]
        if digit not in TRITS:
            raise ValueError(f"section trit must be a trit, got {digit}")
        return digit
    raise ValueError(f"unknown expanding-D control {control!r}")


@dataclass(frozen=True)
class ExpandingDResidueSpec:
    """Observational residual: current LSD of ``T_λ``."""

    gain: int = 1
    start_remaining: int = INPUT_LENGTH
    name: str = "expanding_d"
    dimension: int = 1

    def __post_init__(self) -> None:
        if self.gain < 1:
            raise ValueError("gain must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.gain != 1 and self.name == "expanding_d":
            object.__setattr__(self, "name", f"expanding_d_gain_{self.gain}")

    @property
    def initial_state(self) -> State:
        return (0,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        return (apply_control(state[0], control, self.gain),)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del phase
        return apply_control(state[0], control, self.gain)

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
        return phase.value == 0 and state == (0,)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        """``I_a`` resets; ``T`` multiplies by a residue unit. Not one ``A``."""
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        """Predecessors under the ``T`` residue map only."""
        target = state[0]
        found = {(residue,) for residue in TRITS if residue_step(residue, self.gain) == target}
        return tuple(sorted(found))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", True)
        kwargs.setdefault("candidate_region", RESIDUES)
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", tuple(sorted(RESIDUES)))
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


@dataclass(frozen=True)
class ExpandingDIntegerSpec:
    """Question A: integer state under ``T``. Expected to hit the closure cap."""

    start: int = 1
    gain: int = 1
    start_remaining: int = 32
    name: str = "expanding_d_integer"
    dimension: int = 1

    def __post_init__(self) -> None:
        if self.gain < 1:
            raise ValueError("gain must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")

    @property
    def initial_state(self) -> State:
        return (self.start,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return (expanding_d(state[0], self.gain),)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value > 0:
            return (T_CONTROL,)
        return ()

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del state
        return phase.value > 0

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del state
        return False

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", 16)
        return AttackContext(**kwargs)


def expanding_d_spec(
    start_remaining: int = INPUT_LENGTH,
    gain: int = 1,
) -> ExpandingDResidueSpec:
    return ExpandingDResidueSpec(gain=gain, start_remaining=start_remaining)


def mealy_step(state: State, control: object, gain: int = 1) -> tuple[State, int]:
    nxt = apply_control(state[0], control, gain)
    return (nxt,), nxt


def raw_state_count(states: frozenset[State] = RESIDUES) -> int:
    return len(states)


def minimized_state_count(
    states: frozenset[State] = RESIDUES,
    gain: int = 1,
) -> int:
    def step(state: State, control: object) -> tuple[State, int]:
        return mealy_step(state, control, gain)

    return minimize_mealy_count(states, CONTROLS, step)


def output_signatures(
    states: frozenset[State] = RESIDUES,
    gain: int = 1,
) -> dict[State, tuple[int, ...]]:
    return {
        state: tuple(mealy_step(state, control, gain)[1] for control in CONTROLS)
        for state in sorted(states)
    }


def mealy_classes(
    states: frozenset[State] = RESIDUES,
    gain: int = 1,
) -> tuple[frozenset[State], ...]:
    def step(state: State, control: object) -> tuple[State, int]:
        return mealy_step(state, control, gain)

    return mealy_partition(states, CONTROLS, step)
