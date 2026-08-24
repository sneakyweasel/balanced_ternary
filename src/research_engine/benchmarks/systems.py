"""Five synthetic dynamics with known behavior.

These are engine regression systems, not Ostrowski numeration.
A bounded census is still not an asymptotic theorem.
"""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.affine_system import AffineSystem
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State


@dataclass(frozen=True)
class FiniteClosureSpec:
    """A: collapse to 0. Finite live set {(0,)}."""

    name: str = "benchmark_finite_closure"
    dimension: int = 1
    initial_state: State = (0,)
    start_remaining: int = 3

    def transition(self, state: State, control: int, phase: IntPhase) -> State:
        del state, control, phase
        return (0,)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[int, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (0,)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return IntPhase(phase.value - 1)

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del phase
        return state == (0,)

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        return phase.value == 0 and state == (0,)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return tuple(state)


@dataclass(frozen=True)
class InfiniteTranslateSpec:
    """B: x |-> x+1, always live. Infinite live family x_n = n."""

    name: str = "benchmark_infinite_translate"
    dimension: int = 1
    initial_state: State = (0,)

    def transition(self, state: State, control: int, phase: IntPhase) -> State:
        del control, phase
        return (state[0] + 1,)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[int, ...]:
        del state, phase
        return (1,)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del state, phase
        return True

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del state, phase
        return False

    def initial_phase(self) -> IntPhase:
        return IntPhase(0)

    def canonicalize(self, state: State) -> State:
        return tuple(state)


@dataclass(frozen=True)
class ResetLoopSpec:
    """C: 0→0 under two letters. Infinite words, finite terminals {0}."""

    name: str = "benchmark_reset_loop"
    dimension: int = 1
    initial_state: State = (0,)

    def transition(self, state: State, control: int, phase: IntPhase) -> State:
        del state, control, phase
        return (0,)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[int, ...]:
        del state, phase
        return (0, 1)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del phase
        return state == (0,)

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del phase
        return state == (0,)

    def initial_phase(self) -> IntPhase:
        return IntPhase(0)

    def canonicalize(self, state: State) -> State:
        return tuple(state)


@dataclass(frozen=True)
class ModularTripleSpec:
    """D: x |-> 3x. Images are 0 mod 3."""

    name: str = "benchmark_modular_triple"
    dimension: int = 1
    initial_state: State = (1,)
    start_remaining: int = 3

    def transition(self, state: State, control: int, phase: IntPhase) -> State:
        del control, phase
        return (3 * state[0],)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[int, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (0,)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return IntPhase(phase.value - 1)

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del state, phase
        return True

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        return phase.value == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return tuple(state)


@dataclass(frozen=True)
class ExpandingEscapeSpec:
    """E: x |-> 2x expands, but |x|>1 leaves the live region."""

    name: str = "benchmark_expanding_escape"
    dimension: int = 1
    initial_state: State = (1,)
    start_remaining: int = 4

    def transition(self, state: State, control: int, phase: IntPhase) -> State:
        del control, phase
        return (2 * state[0],)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[int, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (0,)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return IntPhase(phase.value - 1)

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del phase
        return abs(state[0]) <= 1

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        return phase.value == 0 and abs(state[0]) <= 1

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return tuple(state)


def affine_finite_closure() -> AffineSystem:
    return AffineSystem(A=((0,),), translations={0: (0,)})


def affine_translate() -> AffineSystem:
    return AffineSystem(A=((1,),), translations={1: (1,)})


def affine_reset_loop() -> AffineSystem:
    return AffineSystem(A=((0,),), translations={0: (0,), 1: (0,)})


def affine_triple() -> AffineSystem:
    return AffineSystem(A=((3,),), translations={0: (0,)})


def affine_expand() -> AffineSystem:
    return AffineSystem(A=((2,),), translations={0: (0,)})


def context_finite_closure() -> AttackContext:
    return AttackContext(
        live_only=True,
        affine=affine_finite_closure(),
        candidate_region=frozenset({(0,)}),
        word=(0,),
        functional=LinearFunctional((1,)),
    )


def context_infinite_translate(*, max_steps: int = 8) -> AttackContext:
    return AttackContext(
        live_only=True,
        affine=affine_translate(),
        word=(1,),
        functional=LinearFunctional((1,)),
        max_steps=max_steps,
    )


def context_reset_loop() -> AttackContext:
    return AttackContext(
        live_only=True,
        affine=affine_reset_loop(),
        candidate_region=frozenset({(0,)}),
        word=(0, 1, 0),
        functional=LinearFunctional((1,)),
    )


def context_modular_triple() -> AttackContext:
    return AttackContext(
        live_only=True,
        affine=affine_triple(),
        word=(0,),
        functional=LinearFunctional((1,)),
    )


def context_expanding_escape() -> AttackContext:
    return AttackContext(
        live_only=True,
        affine=affine_expand(),
        candidate_region=frozenset({(0,), (1,), (-1,)}),
        word=(0,),
        functional=LinearFunctional((1,)),
    )
