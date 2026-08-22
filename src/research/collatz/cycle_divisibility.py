"""Divisibility of C by D = 2^K - 3^p for periodic exponent codes.

If ``q`` divides ``D`` and ``q ≠ 3``, then in ``F_q``

    λ_j = 2^{K_j} 3^{-j},    λ_p = 1,

and ``q | C`` if and only if ``sum_{j < p} λ_j = 0``. This is the
divisor-specific finite-field walk; it is not a universal residue pin
on ``C``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from research.collatz.cylinders import parse_ks
from research.collatz.itinerary import ValuationItinerary


def cycle_divisor(code: tuple[int, ...] | str | list[int]) -> int:
    it = ValuationItinerary.from_ks(code)
    return it.denominator - it.numerator_multiplier


def gcd_C_D(code: tuple[int, ...] | str | list[int]) -> int:
    it = ValuationItinerary.from_ks(code)
    D = it.denominator - it.numerator_multiplier
    return math.gcd(it.C, abs(D))


def trial_prime_factors(n: int, limit: int = 10_000) -> tuple[tuple[int, int], int]:
    """Factor ``|n|`` by trial division up to ``limit``.

    Returns ``(prime_powers, cofactor)``. The cofactor is 1 if fully factored
    inside the bound, otherwise the unfactored remainder.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int")
    value = abs(n)
    if value == 0:
        return (), 0
    factors: list[tuple[int, int]] = []
    remaining = value
    p = 2
    while p * p <= remaining and p <= limit:
        if remaining % p == 0:
            exp = 0
            while remaining % p == 0:
                remaining //= p
                exp += 1
            factors.append((p, exp))
        p = 3 if p == 2 else p + 2
    return tuple(factors), remaining


def finite_field_walk_sum(code: tuple[int, ...], q: int) -> int:
    """``sum_j 2^{K_j} 3^{-j}`` in ``F_q``. Requires ``q`` prime, ``q ≠ 3``."""
    if q < 2:
        raise ValueError("q must be a prime >= 2")
    ks = parse_ks(code)
    p = len(ks)
    three_inv = pow(3, -1, q)
    total = 0
    lam = 1  # λ_0 = 1
    K = 0
    for j, k in enumerate(ks):
        total = (total + lam) % q
        K += k
        lam = (lam * pow(2, k, q) * three_inv) % q
    if p == 0:
        return 0
    return total


def walk_vanishes(code: tuple[int, ...], q: int) -> bool:
    return finite_field_walk_sum(code, q) == 0


@dataclass(frozen=True)
class DivisibilityReport:
    code: tuple[int, ...]
    C: int
    D: int
    gcd: int
    D_divides_C: bool
    small_factors_of_D: tuple[tuple[int, int], ...]
    D_cofactor: int
    obstructing_primes: tuple[int, ...]
    walk_sums: tuple[tuple[int, int], ...]
    status: str

    def as_dict(self) -> dict[str, object]:
        return {
            "code": list(self.code),
            "C": self.C,
            "D": self.D,
            "gcd": self.gcd,
            "D_divides_C": self.D_divides_C,
            "small_factors_of_D": [list(pair) for pair in self.small_factors_of_D],
            "D_cofactor": self.D_cofactor,
            "obstructing_primes": list(self.obstructing_primes),
            "walk_sums": [list(pair) for pair in self.walk_sums],
            "status": self.status,
        }


def divisibility_report(code: tuple[int, ...] | str | list[int]) -> DivisibilityReport:
    ks = parse_ks(code)
    it = ValuationItinerary.from_ks(ks)
    D = it.denominator - it.numerator_multiplier
    g = math.gcd(it.C, abs(D))
    divides = D != 0 and it.C % D == 0
    factors, cofactor = trial_prime_factors(D)
    walks = []
    obstructing = []
    for q, _exp in factors:
        if q == 3:
            continue
        s = finite_field_walk_sum(ks, q)
        walks.append((q, s))
        if s != 0:
            obstructing.append(q)
    status = "EXACT gcd and exact C mod D; walks only for trial primes"
    return DivisibilityReport(
        code=ks,
        C=it.C,
        D=D,
        gcd=g,
        D_divides_C=divides,
        small_factors_of_D=factors,
        D_cofactor=cofactor,
        obstructing_primes=tuple(obstructing),
        walk_sums=tuple(walks),
        status=status,
    )


def christoffel_binary(N: int, r: int) -> tuple[int, ...]:
    """Fernández–Ibáñez / ceiling Christoffel word of length ``N`` with ``r`` ones."""
    if isinstance(N, bool) or not isinstance(N, int) or N < 1:
        raise ValueError("N must be an integer >= 1")
    if isinstance(r, bool) or not isinstance(r, int) or r < 0 or r > N:
        raise ValueError("r must be an integer in [0, N]")
    return tuple(
        math.ceil(i * r / N) - math.ceil((i - 1) * r / N) for i in range(1, N + 1)
    )


def christoffel_exponent_code(p: int, K: int) -> tuple[int, ...]:
    """Accelerated code of the Syracuse Christoffel word of parameters ``(K, p)``."""
    from research.collatz.amplitude import exponent_code_from_syracuse

    bits = christoffel_binary(K, p)
    if bits[0] != 1:
        # rotate until an odd Syracuse step starts the word
        for i, bit in enumerate(bits):
            if bit == 1:
                bits = bits[i:] + bits[:i]
                break
        else:
            raise ValueError("Christoffel word has no odd step")
    return exponent_code_from_syracuse(bits)


def is_balanced_binary(bits: tuple[int, ...]) -> bool:
    """Classical balance: factor one-counts differ by at most 1."""
    n = len(bits)
    for length in range(1, n + 1):
        counts = []
        doubled = bits + bits
        for start in range(n if length < n else 1):
            window = doubled[start : start + length]
            if length == n and start:
                continue
            counts.append(sum(window))
        if counts and max(counts) - min(counts) > 1:
            return False
    return True
