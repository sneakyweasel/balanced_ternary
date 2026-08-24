"""Immutable and lazy trajectories of a ``ProblemSpec``.

Do not store complete state lists for massive searches unless requested.
A trajectory records controls; states and phases are derived or stored
explicitly after materialization.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

from research_engine.core.problem_spec import ProblemSpec

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


def _as_tuple(values: Sequence[object]) -> tuple:
    return tuple(values)


@dataclass(frozen=True)
class Trajectory(Generic[S, C, P]):
    """Materialized trajectory.

    ``states[0]`` and ``phases[0]`` are the initial configuration.
    ``len(states) == len(phases) == len(controls) + 1``.
    """

    initial_state: S
    initial_phase: P
    controls: tuple[C, ...]
    states: tuple[S, ...]
    phases: tuple[P, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "controls", _as_tuple(self.controls))
        object.__setattr__(self, "states", _as_tuple(self.states))
        object.__setattr__(self, "phases", _as_tuple(self.phases))
        if len(self.states) != len(self.controls) + 1:
            raise ValueError("states must include the initial state and one state per control")
        if len(self.phases) != len(self.controls) + 1:
            raise ValueError("phases must include the initial phase and one phase per control")
        if self.states[0] != self.initial_state:
            raise ValueError("states[0] must equal initial_state")
        if self.phases[0] != self.initial_phase:
            raise ValueError("phases[0] must equal initial_phase")

    def state_at(self, index: int) -> S:
        return self.states[index]

    def phase_at(self, index: int) -> P:
        return self.phases[index]

    def prefix(self, index: int) -> Trajectory[S, C, P]:
        if index < 0 or index > len(self.controls):
            raise IndexError("prefix index out of range")
        return Trajectory(
            initial_state=self.initial_state,
            initial_phase=self.initial_phase,
            controls=self.controls[:index],
            states=self.states[: index + 1],
            phases=self.phases[: index + 1],
        )

    def suffix(self, index: int) -> Trajectory[S, C, P]:
        if index < 0 or index > len(self.controls):
            raise IndexError("suffix index out of range")
        return Trajectory(
            initial_state=self.states[index],
            initial_phase=self.phases[index],
            controls=self.controls[index:],
            states=self.states[index:],
            phases=self.phases[index:],
        )

    def terminal_state(self) -> S:
        return self.states[-1]

    def is_legal(self, spec: ProblemSpec[S, C, P]) -> bool:
        if spec.canonicalize(self.initial_state) != spec.canonicalize(self.states[0]):
            return False
        state = self.states[0]
        phase = self.phases[0]
        for i, control in enumerate(self.controls):
            if control not in spec.legal_controls(state, phase):
                return False
            expected_state = spec.canonicalize(spec.transition(state, control, phase))
            expected_phase = spec.next_phase(phase, control)
            state = self.states[i + 1]
            phase = self.phases[i + 1]
            if spec.canonicalize(state) != expected_state or phase != expected_phase:
                return False
        return True


class LazyTrajectory(Generic[S, C, P]):
    """Iterator over configurations; states are not stored unless materialized."""

    def __init__(
        self,
        spec: ProblemSpec[S, C, P],
        controls: Sequence[C],
        *,
        initial_state: S | None = None,
        initial_phase: P | None = None,
    ) -> None:
        self.spec = spec
        self.controls = tuple(controls)
        self.initial_state = spec.canonicalize(
            spec.initial_state if initial_state is None else initial_state
        )
        self.initial_phase = spec.initial_phase() if initial_phase is None else initial_phase

    def configurations(self) -> Iterator[tuple[S, P]]:
        state = self.initial_state
        phase = self.initial_phase
        yield state, phase
        for control in self.controls:
            state = self.spec.canonicalize(self.spec.transition(state, control, phase))
            phase = self.spec.next_phase(phase, control)
            yield state, phase

    def is_legal(self) -> bool:
        state = self.initial_state
        phase = self.initial_phase
        for control in self.controls:
            if control not in self.spec.legal_controls(state, phase):
                return False
            state = self.spec.canonicalize(self.spec.transition(state, control, phase))
            phase = self.spec.next_phase(phase, control)
        return True

    def terminal_state(self) -> S:
        state = self.initial_state
        phase = self.initial_phase
        for control in self.controls:
            state = self.spec.canonicalize(self.spec.transition(state, control, phase))
            phase = self.spec.next_phase(phase, control)
        return state

    def materialize(self) -> Trajectory[S, C, P]:
        states: list[S] = []
        phases: list[P] = []
        for state, phase in self.configurations():
            states.append(state)
            phases.append(phase)
        return Trajectory(
            initial_state=self.initial_state,
            initial_phase=self.initial_phase,
            controls=self.controls,
            states=tuple(states),
            phases=tuple(phases),
        )


def simulate(
    spec: ProblemSpec[S, C, P],
    controls: Sequence[C],
    *,
    store_states: bool = True,
) -> Trajectory[S, C, P] | LazyTrajectory[S, C, P]:
    lazy = LazyTrajectory(spec, controls)
    if store_states:
        return lazy.materialize()
    return lazy
