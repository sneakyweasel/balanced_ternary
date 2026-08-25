"""Section maps as ``ProblemSpec`` adapters. No PrimeEngine."""

from __future__ import annotations

from dataclasses import dataclass

from bt.arithmetic import is_prime
from research.prime_residual_complexity.sections import TRITS, apply_section_word, predecessor
from research.prime_residual_complexity.sieve import (
    DEFAULT_SIEVE,
    is_coprime,
    predecessors_mod,
    sieve_modulus,
    step_mod,
)
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.affine_system import AffineSystem
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

DEFAULT_DEPTH = 4
PRIME_STATE_CAP = 16
REVERSE_DEPTH_CAP = 6

SECTION_AFFINE = AffineSystem(
    A=((3,),),
    translations={digit: (digit,) for digit in TRITS},
    controls=TRITS,
)


@dataclass(frozen=True)
class SieveSpec:
    """Finite residual ``n mod M`` for ``gcd(n, M)=1`` under ``I_a``."""

    primes: tuple[int, ...] = DEFAULT_SIEVE
    start: int = 0
    start_remaining: int = DEFAULT_DEPTH
    name: str = "prime_residual_complexity"
    dimension: int = 1

    def __post_init__(self) -> None:
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        object.__setattr__(self, "primes", tuple(int(p) for p in self.primes))

    @property
    def modulus(self) -> int:
        return sieve_modulus(self.primes)

    @property
    def initial_state(self) -> State:
        return (self._reduce(self.start),)

    def _reduce(self, n: int) -> int:
        return int(n) % self.modulus

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        return (step_mod(state[0], int(control), self.modulus),)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value <= 0:
            return ()
        return TRITS

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del state, phase
        return False

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del phase
        return is_coprime(state[0], self.modulus)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> bool:
        del control
        current = phase if phase is not None else self.initial_phase()
        return self.is_accepting(state, current)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (self._reduce(state[0]),)

    def affine_system(self) -> AffineSystem:
        return SECTION_AFFINE

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        return tuple((pred,) for pred in predecessors_mod(state[0], self.modulus))

    @property
    def candidate_region(self) -> frozenset[State]:
        return frozenset((residue,) for residue in range(self.modulus))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", max(256, self.modulus + 1))
        kwargs.setdefault("max_steps", max(1, self.start_remaining))
        kwargs.setdefault("affine", self.affine_system())
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("candidate_region", self.candidate_region)
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault(
            "reverse_seeds",
            tuple((residue,) for residue in range(self.modulus) if is_coprime(residue, self.modulus)),
        )
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


@dataclass(frozen=True)
class PrimeSpec:
    """Integer section dynamics with the prime predicate as acceptance."""

    start: int = 1
    start_remaining: int = DEFAULT_DEPTH
    state_cap: int = PRIME_STATE_CAP
    reverse_max_depth: int = REVERSE_DEPTH_CAP
    name: str = "prime_residual_complexity_integer"
    dimension: int = 1

    def __post_init__(self) -> None:
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")

    @property
    def initial_state(self) -> State:
        return (int(self.start),)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del phase
        return (apply_section_word(state[0], (int(control),)),)

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value <= 0:
            return ()
        return TRITS

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del state, phase
        return False

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del phase
        return is_prime(state[0])

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> bool:
        del control
        current = phase if phase is not None else self.initial_phase()
        return self.is_accepting(state, current)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self) -> AffineSystem:
        return SECTION_AFFINE

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        return ((predecessor(state[0]),),)

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", max(1, self.start_remaining))
        kwargs.setdefault("affine", self.affine_system())
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", ((2,), (3,)))
        kwargs.setdefault("reverse_max_depth", self.reverse_max_depth)
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def sieve_spec(
    start_remaining: int = DEFAULT_DEPTH,
    primes: tuple[int, ...] = DEFAULT_SIEVE,
    start: int = 0,
) -> SieveSpec:
    return SieveSpec(primes=primes, start=start, start_remaining=start_remaining)


def prime_spec(
    start_remaining: int = DEFAULT_DEPTH,
    start: int = 1,
    state_cap: int = PRIME_STATE_CAP,
) -> PrimeSpec:
    return PrimeSpec(start=start, start_remaining=start_remaining, state_cap=state_cap)
