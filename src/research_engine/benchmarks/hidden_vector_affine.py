"""Hidden 2-D vector-affine maps. Matrices and domains are not part of the spec."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State


def _v2(n: int) -> int:
    if n == 0:
        return 0
    value = abs(n)
    k = 0
    while value % 2 == 0:
        value //= 2
        k += 1
    return k


def _finite_alphabet(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    if x % 2 == 0:
        return (x + 1, y)
    return (-y, x)


def _parameterized_shear(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = _v2(abs(x) + 1)
    return (x + k * y + 1, y + 1)


def _domain_coupled_shear(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = _v2(x - y)
    return (x + k * y, y)


def _false_affine_trap(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    if max(abs(x), abs(y)) <= 8:
        return (x, y)
    return (2 * x, 2 * y)


def _parity_shear(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    if (x + y) % 2 == 0:
        return (x + y, y)
    return (x, x + y)


@dataclass(frozen=True)
class HiddenVectorSpec:
    """Singleton-control 2-D integer map. The transition is the only exposed law."""

    name: str
    start: tuple[int, int] = (1, 1)
    start_remaining: int = 8
    dimension: int = 2

    def _step(self, state: State) -> State:
        raise NotImplementedError

    @property
    def initial_state(self) -> State:
        return (int(self.start[0]), int(self.start[1]))

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return self._step(state)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (0,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del state
        return phase.value >= 0

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del state
        return phase.value == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]), int(state[1]))

    def affine_system(self):
        return None

    def attack_context(self) -> AttackContext:
        return AttackContext(live_only=False, max_states=32, max_steps=self.start_remaining)


@dataclass(frozen=True)
class HiddenFiniteAlphabetSpec(HiddenVectorSpec):
    name: str = "hidden_vector_finite"

    def _step(self, state: State) -> State:
        return _finite_alphabet(state)


@dataclass(frozen=True)
class HiddenParameterizedMatrixSpec(HiddenVectorSpec):
    name: str = "hidden_vector_parameterized"

    def _step(self, state: State) -> State:
        return _parameterized_shear(state)


@dataclass(frozen=True)
class HiddenDomainCoupledSpec(HiddenVectorSpec):
    name: str = "hidden_vector_domain_coupled"

    def _step(self, state: State) -> State:
        return _domain_coupled_shear(state)


@dataclass(frozen=True)
class HiddenFalseAffineTrapSpec(HiddenVectorSpec):
    name: str = "hidden_vector_trap"

    def _step(self, state: State) -> State:
        return _false_affine_trap(state)


@dataclass(frozen=True)
class HiddenParityShearSpec(HiddenVectorSpec):
    """Unrelated 2-D lattice map. Independent of remainder dynamics."""

    name: str = "hidden_vector_parity_shear"

    def _step(self, state: State) -> State:
        return _parity_shear(state)
