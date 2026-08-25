"""Two-trit product residual as a ``ProblemSpec``. No product engine."""

from __future__ import annotations

from dataclasses import dataclass

from bt.transducers.mealy import minimize_mealy_count
from research.multiplicative_residual.discovery import (
    pair_controls,
    product_step,
    reachable_product,
)
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

INPUT_LENGTH = 8


@dataclass(frozen=True)
class ProductResidualSpec:
    """LSD-first residual of ``λ·D(s+d1 d2)`` with trit pairs as controls."""

    gain: int = 1
    scale: int = 1
    start_remaining: int = INPUT_LENGTH
    name: str = "multiplicative_residual"
    dimension: int = 1

    def __post_init__(self) -> None:
        if self.gain < 1:
            raise ValueError("gain must be a positive integer")
        if self.scale < 1:
            raise ValueError("scale must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if (self.gain, self.scale) != (1, 1) and self.name == "multiplicative_residual":
            object.__setattr__(
                self, "name", f"multiplicative_residual_g{self.gain}_s{self.scale}"
            )

    @property
    def controls(self) -> tuple[tuple[int, int], ...]:
        return pair_controls()

    @property
    def candidate_region(self) -> frozenset[State]:
        reached = reachable_product(self.controls, self.gain, self.scale)
        if reached is None:
            return frozenset()
        return frozenset((s,) for s in reached)

    @property
    def initial_state(self) -> State:
        return (0,)

    def emit(self, residual: int, control: tuple[int, int]) -> tuple[int, int]:
        return product_step(residual, control, self.gain, self.scale)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        left, right = control  # type: ignore[misc]
        nxt, _out = self.emit(state[0], (left, right))
        return (nxt,)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del phase
        left, right = control  # type: ignore[misc]
        _nxt, out = self.emit(state[0], (left, right))
        return out

    def raw_contribution(self, control: object) -> int:
        left, right = control  # type: ignore[misc]
        return self.scale * left * right

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value > 0:
            return self.controls
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
        nxt, _out = self.emit(state[0], (0, 0))
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
        if not region:
            return ()
        for residual in region:
            for control in self.controls:
                nxt, _out = product_step(residual, control, self.gain, self.scale)
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


def product_spec(
    start_remaining: int = INPUT_LENGTH,
    gain: int = 1,
    scale: int = 1,
) -> ProductResidualSpec:
    return ProductResidualSpec(
        gain=gain, scale=scale, start_remaining=start_remaining
    )


def raw_state_count(gain: int = 1, scale: int = 1) -> int:
    reached = reachable_product(pair_controls(), gain, scale)
    if reached is None:
        raise RuntimeError("reachable set exceeded the cap")
    return len(reached)


def minimized_state_count(gain: int = 1, scale: int = 1) -> int:
    controls = pair_controls()
    reached = reachable_product(controls, gain, scale)
    if reached is None:
        raise RuntimeError("reachable set exceeded the cap")
    states = frozenset((s,) for s in reached)

    def mealy(state: State, control: object) -> tuple[State, int]:
        left, right = control  # type: ignore[misc]
        nxt, out = product_step(state[0], (left, right), gain, scale)
        return (nxt,), out

    return minimize_mealy_count(states, controls, mealy)
