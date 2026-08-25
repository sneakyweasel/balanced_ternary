"""Hidden vector-affine maps for matrix-word invariant discovery.

Ground-truth moduli, lattices, and exception sets are not part of the
spec. Matrices appear only in the transition.
"""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.attacks.result import AttackContext
from research_engine.benchmarks.hidden_vector_affine import HiddenVectorSpec
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


def _modular_lattice(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = _v2(abs(x) + 1)
    return (x + 2 * k * y, y + 1)


def _gcd_family(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = 2 * _v2(abs(x) + 1)
    return (x + k * y + 1, y)


def _smith_family(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = _v2(abs(x) + 1)
    return (2 * x + 1, (2 + 2 * k) * y + 1)


def _recursive_shear(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = _v2(abs(x) + 1)
    return (x + k * y, y + 1)


def _exceptions(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = _v2(abs(x) + 1)
    return (x + k * y + 1, y)


def _false_trap(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = 2 * _v2(abs(x) + 1) if max(abs(x), abs(y)) <= 8 else 1
    return (x + k * y + 1, y)


def _realizable(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    k = _v2(abs(x) + 1)
    return (x + k * y, y)


def _lattice_walk(state: State) -> State:
    x, y = int(state[0]), int(state[1])
    return (x + 2 * y + 1, 2 * x + y)


@dataclass(frozen=True)
class HiddenModularLatticeSpec(HiddenVectorSpec):
    name: str = "hidden_matrix_modular_lattice"

    def _step(self, state: State) -> State:
        return _modular_lattice(state)


@dataclass(frozen=True)
class HiddenGcdFamilySpec(HiddenVectorSpec):
    name: str = "hidden_matrix_gcd_family"

    def _step(self, state: State) -> State:
        return _gcd_family(state)


@dataclass(frozen=True)
class HiddenSmithFamilySpec(HiddenVectorSpec):
    name: str = "hidden_matrix_smith_family"

    def _step(self, state: State) -> State:
        return _smith_family(state)


@dataclass(frozen=True)
class HiddenRecursiveShearSpec(HiddenVectorSpec):
    name: str = "hidden_matrix_recursive_shear"

    def _step(self, state: State) -> State:
        return _recursive_shear(state)


@dataclass(frozen=True)
class HiddenExceptionSpec(HiddenVectorSpec):
    name: str = "hidden_matrix_exceptions"

    def _step(self, state: State) -> State:
        return _exceptions(state)


@dataclass(frozen=True)
class HiddenFalseInvariantSpec(HiddenVectorSpec):
    name: str = "hidden_matrix_false_invariant"

    def _step(self, state: State) -> State:
        return _false_trap(state)


@dataclass(frozen=True)
class HiddenRealizableFamilySpec(HiddenVectorSpec):
    name: str = "hidden_matrix_realizable"

    def _step(self, state: State) -> State:
        return _realizable(state)


@dataclass(frozen=True)
class HiddenLatticeWalkSpec(HiddenVectorSpec):
    """Unrelated 2-D affine walk. Independent of remainder dynamics."""

    name: str = "hidden_matrix_lattice_walk"

    def _step(self, state: State) -> State:
        return _lattice_walk(state)

    def attack_context(self) -> AttackContext:
        return AttackContext(live_only=False, max_states=32, max_steps=self.start_remaining)
