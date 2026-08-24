"""Spectral classification of constant-coefficient order-3 Gamma-systems.

Floating-point is used only to label roots (Pisot / Perron / neither).
State membership and liveness stay exact integers elsewhere.
"""

from __future__ import annotations

import cmath

from research.ostrowski.adder_search import polynomial_is_irreducible_cubic
from research.ostrowski.system import OstrowskiSystem, characteristic_poly_coeffs


def constant_digits(system: OstrowskiSystem) -> tuple[int, int, int] | None:
    """``(d_1, d_2, d_3)`` when every ``α_k`` is purely periodic of length 1."""
    coeffs = characteristic_poly_coeffs(system)
    if coeffs is None or system.order != 3:
        return None
    return (system.d(1, 1), system.d(2, 1), system.d(3, 1))


def _real_root_bisection(a: int, b: int, c: int) -> float:
    """Simple real root of ``x^3 + a x^2 + b x + c = 0`` by bisection."""
    def f(x: float) -> float:
        return ((x + a) * x + b) * x + c

    lo, hi = -32.0, 32.0
    while f(lo) * f(hi) > 0:
        lo *= 2
        hi *= 2
        if hi > 1e6:
            raise ValueError("no sign change for a real root")
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def cubic_roots(coeffs: tuple[int, ...]) -> tuple[complex, complex, complex]:
    """Roots of ``x^3 + a x^2 + b x + c``. Classification only, not a proof."""
    if len(coeffs) != 4 or coeffs[0] != 1:
        raise ValueError("expected monic cubic coefficients")
    _, a, b, c = coeffs
    lam = _real_root_bisection(a, b, c)
    # Synthetic division: x^2 + (a+λ)x + (b+λ(a+λ))
    p = a + lam
    q = b + lam * p
    disc = p * p - 4.0 * q
    sqrt_disc = cmath.sqrt(disc)
    r1 = (-p + sqrt_disc) / 2.0
    r2 = (-p - sqrt_disc) / 2.0
    return (complex(lam), r1, r2)


def spectral_data(system: OstrowskiSystem) -> dict[str, object]:
    """Irreducibility, roots, and Pisot/Perron labels. Floats are labels only."""
    coeffs = characteristic_poly_coeffs(system)
    digits = constant_digits(system)
    if coeffs is None or digits is None:
        return {
            "constant_coefficient": False,
            "characteristic_polynomial": coeffs,
            "digits": digits,
        }
    irreducible = polynomial_is_irreducible_cubic(coeffs)
    roots = cubic_roots(coeffs) if irreducible else ()
    moduli = tuple(abs(z) for z in roots)
    real_parts = tuple(z.real for z in roots)
    dominant = max(moduli) if moduli else None
    pisot = False
    perron = False
    real_gt_one = [z for z in roots if abs(z.imag) < 1e-10 and z.real > 1 + 1e-10]
    if len(real_gt_one) == 1 and len(roots) == 3:
        alpha = real_gt_one[0].real
        others = [
            abs(z)
            for z in roots
            if not (abs(z.imag) < 1e-10 and abs(z.real - alpha) < 1e-8)
        ]
        pisot = all(m < 1 - 1e-8 for m in others)
        perron = all(m < alpha - 1e-8 for m in others)
    return {
        "constant_coefficient": True,
        "digits": digits,
        "characteristic_polynomial": coeffs,
        "irreducible_cubic": irreducible,
        "roots": roots,
        "moduli": moduli,
        "real_parts": real_parts,
        "dominant_modulus": dominant,
        "pisot": pisot,
        "perron": perron,
        "label": (
            "Pisot"
            if pisot
            else "Perron non-Pisot"
            if perron and not pisot
            else "not Perron"
        ),
    }


def monic_cubic_discriminant(a: int, b: int, c: int) -> int:
    """Discriminant of ``x^3 + a x^2 + b x + c``. Integer, exact."""
    return 18 * a * b * c - 4 * a**3 * c + a**2 * b**2 - 4 * b**3 - 27 * c**2


def eval_monic_cubic(a: int, b: int, c: int, x: int) -> int:
    return ((x + a) * x + b) * x + c


def exact_pisot_cubic_certificate(coeffs: tuple[int, ...]) -> dict[str, object]:
    """Integer-only Pisot / Perron-non-Pisot certificate for a monic cubic.

    Uses: no rational root; discriminant sign (one real root iff Δ<0);
    a sign-change isolating the real root in an open interval ``(p, p+1)``
    with ``p>=2``; product of roots ``-c``. Then conjugate modulus squared
    is ``(-c)/λ``, compared with 1 by comparing ``-c`` with the isolating
    interval. Floating roots are not used.
    """
    if len(coeffs) != 4 or coeffs[0] != 1:
        raise ValueError("expected monic cubic")
    _, a, b, c = coeffs
    irreducible = polynomial_is_irreducible_cubic(coeffs)
    disc = monic_cubic_discriminant(a, b, c)
    one_real_two_complex = disc < 0
    product = -c
    # Isolate the unique real root in (lo, lo+1) for lo = 2,3,... when possible.
    lo = None
    if one_real_two_complex:
        for n in range(1, 16):
            if eval_monic_cubic(a, b, c, n) < 0 < eval_monic_cubic(a, b, c, n + 1):
                lo = n
                break
    # |μ|^2 = product/λ. If λ ∈ (lo, lo+1) and product > lo+1 then |μ|^2 > 1.
    # If product <= lo then |μ|^2 < 1.
    conjugates_outside = False
    conjugates_inside = False
    if lo is not None and product > 0:
        conjugates_outside = product >= lo + 1
        conjugates_inside = product <= lo
    perron = one_real_two_complex and lo is not None and lo >= 1
    pisot = bool(irreducible and perron and conjugates_inside)
    nonpisot_perron = bool(irreducible and perron and conjugates_outside)
    return {
        "irreducible": irreducible,
        "discriminant": disc,
        "one_real_two_complex": one_real_two_complex,
        "real_root_interval": (lo, lo + 1) if lo is not None else None,
        "product_of_roots": product,
        "conjugates_inside_unit_disk": conjugates_inside,
        "conjugates_outside_unit_disk": conjugates_outside,
        "pisot": pisot,
        "perron_non_pisot": nonpisot_perron,
    }
