"""Immutable and lazy trajectories, including phase-dependent legality."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from research_engine.core.phase import IntPhase
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.trajectory import LazyTrajectory, Trajectory, simulate


@dataclass(frozen=True)
class ShiftSpec:
    """One-dimensional shift. Terminal phase uses a strictly smaller alphabet."""

    name: str = "shift_toy"
    dimension: int = 1
    initial_state: tuple[int, ...] = (0,)
    start_remaining: int = 3

    def transition(
        self,
        state: tuple[int, ...],
        control: int,
        phase: IntPhase,
    ) -> tuple[int, ...]:
        del phase
        return (state[0] + control,)

    def legal_controls(self, state: tuple[int, ...], phase: IntPhase) -> tuple[int, ...]:
        del state
        if phase.value <= 0:
            return (0, 1)
        return (-1, 0, 1)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return IntPhase(phase.value - 1)

    def is_terminal(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        del state
        return phase.value <= 0

    def is_accepting(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        return self.is_terminal(state, phase) and state[0] == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(state)


def test_shift_spec_is_a_problem_spec():
    spec = ShiftSpec()
    assert isinstance(spec, ProblemSpec)
    assert spec.legal_controls((0,), spec.initial_phase()) == (-1, 0, 1)
    assert spec.legal_controls((0,), spec.next_phase(spec.next_phase(spec.next_phase(spec.initial_phase(), 0), 0), 0)) == (0, 1)


def test_materialized_trajectory_prefix_suffix_and_terminal():
    spec = ShiftSpec()
    traj = simulate(spec, (1, -1, 0))
    assert isinstance(traj, Trajectory)
    assert traj.states == ((0,), (1,), (0,), (0,))
    assert [phase.value for phase in traj.phases] == [3, 2, 1, 0]
    assert traj.state_at(2) == (0,)
    assert traj.phase_at(3).value == 0
    assert traj.terminal_state() == (0,)
    prefix = traj.prefix(1)
    assert prefix.controls == (1,)
    assert prefix.states == ((0,), (1,))
    suffix = traj.suffix(2)
    assert suffix.initial_state == (0,)
    assert suffix.controls == (0,)
    assert suffix.states == ((0,), (0,))
    assert traj.is_legal(spec)


def test_trajectory_is_immutable():
    traj = simulate(ShiftSpec(), (0,))
    assert isinstance(traj, Trajectory)
    with pytest.raises(AttributeError):
        traj.controls = (1,)  # type: ignore[misc]


def test_illegal_terminal_control_is_detected():
    spec = ShiftSpec(start_remaining=1)
    legal = simulate(spec, (1, 0))
    assert isinstance(legal, Trajectory)
    assert legal.is_legal(spec)
    illegal = Trajectory(
        initial_state=(0,),
        initial_phase=spec.initial_phase(),
        controls=(-1, -1),
        states=((0,), (-1,), (-2,)),
        phases=(spec.initial_phase(), spec.next_phase(spec.initial_phase(), -1), spec.next_phase(spec.next_phase(spec.initial_phase(), -1), -1)),
    )
    assert illegal.is_legal(spec) is False


def test_lazy_trajectory_does_not_require_stored_states():
    spec = ShiftSpec()
    lazy = simulate(spec, (1, -1, 0), store_states=False)
    assert isinstance(lazy, LazyTrajectory)
    assert not hasattr(lazy, "states") or not isinstance(getattr(lazy, "states", None), tuple)
    assert lazy.is_legal()
    assert lazy.terminal_state() == (0,)
    materialized = lazy.materialize()
    assert materialized.states == ((0,), (1,), (0,), (0,))
    assert materialized.is_legal(spec)


def test_empty_trajectory_stays_at_the_origin():
    spec = ShiftSpec()
    traj = simulate(spec, ())
    assert isinstance(traj, Trajectory)
    assert traj.controls == ()
    assert traj.terminal_state() == spec.initial_state
    assert traj.is_legal(spec)
