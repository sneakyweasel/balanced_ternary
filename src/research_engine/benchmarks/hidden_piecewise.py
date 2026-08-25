"""Hidden piecewise-affine integer maps. Branch tables are not part of the spec."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State


def _hidden_congruence_a(x: int) -> int:
    residue = x % 3
    if residue == 0:
        return 2 * x + 1
    if residue == 1:
        return x - 4
    return 3 * x


def _hidden_sign_b(x: int) -> int:
    if x >= 0:
        return 2 * x + 3
    return x - 5


def _hidden_nested_c(x: int) -> int:
    if x % 2 == 0:
        return 2 * x
    residue = x % 6
    if residue == 1:
        return x + 3
    if residue == 3:
        return 3 * x - 1
    return x - 2


def _hidden_power_clear_d(x: int) -> int:
    value = x + 1
    if value == 0:
        return 0
    while value % 2 == 0:
        value //= 2
    return value


def _hidden_odd_prime_clear(x: int) -> int:
    value = x + 1
    if value == 0:
        return 0
    while value % 3 == 0:
        value //= 3
    return value


def _hidden_mixed_residue(x: int) -> int:
    if x % 6 == 2:
        return 3 * x
    return _hidden_power_clear_d(x)


@dataclass(frozen=True)
class HiddenIntegerSpec:
    """Singleton-control integer map. The transition is the only exposed law."""

    name: str
    start: int = 0
    start_remaining: int = 8
    dimension: int = 1

    def _step(self, x: int) -> int:
        raise NotImplementedError

    @property
    def initial_state(self) -> State:
        return (self.start,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return (self._step(int(state[0])),)

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
        return (int(state[0]),)

    def affine_system(self):
        return None

    def attack_context(self) -> AttackContext:
        return AttackContext(live_only=False, max_states=32, max_steps=self.start_remaining)


@dataclass(frozen=True)
class HiddenCongruenceASpec(HiddenIntegerSpec):
    name: str = "hidden_congruence_a"

    def _step(self, x: int) -> int:
        return _hidden_congruence_a(x)


@dataclass(frozen=True)
class HiddenSignBSpec(HiddenIntegerSpec):
    name: str = "hidden_sign_b"

    def _step(self, x: int) -> int:
        return _hidden_sign_b(x)


@dataclass(frozen=True)
class HiddenNestedCSpec(HiddenIntegerSpec):
    name: str = "hidden_nested_c"

    def _step(self, x: int) -> int:
        return _hidden_nested_c(x)


@dataclass(frozen=True)
class HiddenPowerClearDSpec(HiddenIntegerSpec):
    name: str = "hidden_power_clear_d"
    start: int = 1

    def _step(self, x: int) -> int:
        return _hidden_power_clear_d(x)


@dataclass(frozen=True)
class HiddenOddPrimeClearSpec(HiddenIntegerSpec):
    name: str = "hidden_odd_prime_clear"
    start: int = 1

    def _step(self, x: int) -> int:
        return _hidden_odd_prime_clear(x)


@dataclass(frozen=True)
class HiddenMixedResidueSpec(HiddenIntegerSpec):
    name: str = "hidden_mixed_residue"
    start: int = 1

    def _step(self, x: int) -> int:
        return _hidden_mixed_residue(x)


def _hidden_parity_carry(x: int) -> int:
    return 2 * x + (x % 2)


def _hidden_parity_toggle(x: int) -> int:
    if x % 2 == 0:
        return x + 1
    return x - 1


def _hidden_positive_double(x: int) -> int:
    return 2 * x + 1


@dataclass(frozen=True)
class HiddenParityCarrySpec(HiddenIntegerSpec):
    """Finite alphabet synthetic: ``x ↦ 2x + (x mod 2)``."""

    name: str = "hidden_parity_carry"

    def _step(self, x: int) -> int:
        return _hidden_parity_carry(x)


@dataclass(frozen=True)
class HiddenInvolutionESpec(HiddenIntegerSpec):
    """Cycle-bearing synthetic: even/odd toggle, period 2."""

    name: str = "hidden_involution_e"

    def _step(self, x: int) -> int:
        return _hidden_parity_toggle(x)


@dataclass(frozen=True)
class HiddenPositiveDoubleSpec(HiddenIntegerSpec):
    """Algebraic cycle candidate off the nonnegative domain."""

    name: str = "hidden_positive_double"
    start: int = 0

    def _step(self, x: int) -> int:
        return _hidden_positive_double(x)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0 or int(state[0]) < 0:
            return ()
        return (0,)


def _hidden_large_fixed(x: int) -> int:
    return 2 * x + (x % 2) - 100


@dataclass(frozen=True)
class HiddenLargeFixedSpec(HiddenIntegerSpec):
    """Algebraic cycle candidate outside the default sample window."""

    name: str = "hidden_large_fixed"
    start: int = 0

    def _step(self, x: int) -> int:
        return _hidden_large_fixed(x)
