"""Mahler-measure and prime-polynomial scans (research, not core)."""

from __future__ import annotations

import cmath
import math

from bt.polynomials import BTPolynomial, factor_small, polynomial
from bt.representation import encode


def mahler_measure(poly: BTPolynomial, *, samples: int = 4096) -> float:
    """Numerical Mahler measure via Jensen's formula on the unit circle.

    ``M(P) = exp((1/2π) ∫ log|P(e^{iθ})| dθ)``. Not a theorem. Unused if
    ``P`` is zero. Roots on the circle make the integrand singular; a floor
    of ``1e-15`` is used.
    """
    if poly.coeffs == (0,):
        return 0.0
    acc = 0.0
    for j in range(samples):
        theta = 2.0 * math.pi * j / samples
        z = cmath.exp(1j * theta)
        val = 0j
        pow_z = 1 + 0j
        for a in poly.coeffs:
            val += a * pow_z
            pow_z *= z
        acc += math.log(max(abs(val), 1e-15))
    return math.exp(acc / samples)


def prime_polynomial_factors(primes: tuple[int, ...]) -> list[dict[str, object]]:
    """For each prime ``p``, record ``Z[x]`` trial factors of ``P_p``."""
    rows = []
    for p in primes:
        poly = polynomial(p)
        rows.append(
            {
                "p": p,
                "word": encode(p).word(),
                "degree": poly.degree,
                "weight": poly.coefficient_weight(),
                "palindromic": poly.is_palindromic(),
                "factors": factor_small(poly),
                "P(1)": poly.evaluate(1),
                "P(-1)": poly.evaluate(-1),
            }
        )
    return rows
