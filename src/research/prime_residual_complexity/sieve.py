"""Exact modular-sieve DFA on LSD-first sections ``I_a``."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, prod

from bt.automata.minimize import minimize_dfa, reachable_states
from research.prime_residual_complexity.sections import TRITS, apply_section_word

IntSeq = tuple[int, ...] | list[int]

SIEVE_CHAIN: tuple[tuple[int, ...], ...] = (
    (2,),
    (2, 3),
    (2, 3, 5),
    (2, 3, 5, 7),
)
DEFAULT_SIEVE: tuple[int, ...] = (2, 3, 5, 7)


def sieve_modulus(primes: IntSeq = DEFAULT_SIEVE) -> int:
    values = tuple(int(p) for p in primes)
    if not values:
        raise ValueError("sieve must contain at least one prime")
    return int(prod(values))


def is_coprime(n: int, modulus: int) -> bool:
    return gcd(int(n), int(modulus)) == 1


def totient(modulus: int) -> int:
    m = int(modulus)
    return sum(1 for n in range(m) if gcd(n, m) == 1)


def step_mod(residue: int, digit: int, modulus: int) -> int:
    return apply_section_word(int(residue), (int(digit),)) % int(modulus)


def predecessors_mod(residue: int, modulus: int) -> tuple[int, ...]:
    target = int(residue) % int(modulus)
    found: list[int] = []
    for src in range(int(modulus)):
        for digit in TRITS:
            if step_mod(src, digit, modulus) == target:
                found.append(src)
                break
    return tuple(found)


@dataclass(frozen=True)
class SieveCensus:
    primes: tuple[int, ...]
    modulus: int
    raw_states: int
    reachable_states: int
    minimized_states: int
    accepting_states: int
    survival_numerator: int
    survival_denominator: int

    @property
    def survival_density(self) -> tuple[int, int]:
        return (self.survival_numerator, self.survival_denominator)


def sieve_census(primes: IntSeq = DEFAULT_SIEVE) -> SieveCensus:
    sieve = tuple(int(p) for p in primes)
    modulus = sieve_modulus(sieve)

    def delta(state: int, letter: int) -> int:
        return step_mod(state, letter, modulus)

    reachable = reachable_states(0, TRITS, delta)
    accepts = [state for state in reachable if is_coprime(state, modulus)]
    minimized = minimize_dfa(0, TRITS, delta, accepts)
    return SieveCensus(
        primes=sieve,
        modulus=modulus,
        raw_states=modulus,
        reachable_states=len(reachable),
        minimized_states=minimized.state_count,
        accepting_states=len(accepts),
        survival_numerator=totient(modulus),
        survival_denominator=modulus,
    )


def sieve_chain_census() -> tuple[SieveCensus, ...]:
    return tuple(sieve_census(primes) for primes in SIEVE_CHAIN)
