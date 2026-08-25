"""Discovered ``D(x+y)`` residual as a ``ProblemSpec``.

State is the correction ``D(s+a+b)`` of a running residual and two
input digits. The adapter uses existing ``D``/``lsd``, not a carry
lookup table. Bound ``1`` is the balanced trit alphabet. Bound ``2``
is the controlled perturbation.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.transducers.mealy import minimize_mealy_count
from research.balanced_ternary.d_add import step, streaming_reachable
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

INPUT_LENGTH = 8


def alphabet(bound: int) -> tuple[int, ...]:
    return tuple(range(-bound, bound + 1))


def controls(bound: int) -> tuple[tuple[int, int], ...]:
    digits = alphabet(bound)
    return tuple((a, b) for a in digits for b in digits)


@dataclass(frozen=True)
class DAddResidualSpec:
    """Finite-control residual of LSD-first balanced addition."""

    bound: int = 1
    start_remaining: int = INPUT_LENGTH
    name: str = "d_add"
    dimension: int = 1

    def __post_init__(self) -> None:
        if self.bound < 1:
            raise ValueError("bound must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.bound != 1 and self.name == "d_add":
            object.__setattr__(self, "name", f"d_add_bound_{self.bound}")

    @property
    def digits(self) -> tuple[int, ...]:
        return alphabet(self.bound)

    @property
    def candidate_region(self) -> frozenset[State]:
        return frozenset((s,) for s in streaming_reachable(self.digits))

    @property
    def initial_state(self) -> State:
        return (0,)

    def emit(self, residual: int, left: int, right: int) -> tuple[int, int]:
        return step(residual, left, right)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        left, right = control  # type: ignore[misc]
        nxt, _out = self.emit(state[0], left, right)
        return (nxt,)

    def output(self, state: State, control: object) -> int:
        left, right = control  # type: ignore[misc]
        _nxt, out = self.emit(state[0], left, right)
        return out

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value > 0:
            return controls(self.bound)
        if state[0] == 0:
            return ()
        return ((0, 0),)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        if self.is_accepting(state, phase):
            return True
        if phase.value > 0:
            return True
        nxt, _out = self.emit(state[0], 0, 0)
        return abs(nxt) < abs(state[0])

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        return phase.value == 0 and state == (0,)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        target = state[0]
        found: set[State] = set()
        region = {s[0] for s in self.candidate_region}
        for residual in region:
            for left in self.digits:
                for right in self.digits:
                    nxt, _out = step(residual, left, right)
                    if nxt == target:
                        found.add((residual,))
        return tuple(sorted(found))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", True)
        kwargs.setdefault("candidate_region", self.candidate_region)
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", tuple(sorted(self.candidate_region)))
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def d_add_spec(start_remaining: int = INPUT_LENGTH, bound: int = 1) -> DAddResidualSpec:
    return DAddResidualSpec(bound=bound, start_remaining=start_remaining)


def raw_state_count(bound: int = 1) -> int:
    return len(streaming_reachable(alphabet(bound)))


def minimized_state_count(bound: int = 1) -> int:
    digits = alphabet(bound)
    states = frozenset((s,) for s in streaming_reachable(digits))
    ctrls = controls(bound)

    def mealy(state: State, control: object) -> tuple[State, int]:
        left, right = control  # type: ignore[misc]
        nxt, out = step(state[0], left, right)
        return (nxt,), out

    return minimize_mealy_count(states, ctrls, mealy)
