"""Spectral classification of constant-coefficient order-3 Gamma-systems.

Floating-point is used only to label roots (Pisot / Perron / neither).
State membership and liveness stay exact integers elsewhere.
Integer cubic certificates live in ``research_engine.algebra.spectral``.
"""

from __future__ import annotations

from research.ostrowski.system import OstrowskiSystem, characteristic_poly_coeffs
from research_engine.algebra.spectral import (
    cubic_roots,
    exact_pisot_cubic_certificate,
    eval_monic_cubic,
    monic_cubic_discriminant,
    polynomial_is_irreducible_cubic,
)


def constant_digits(system: OstrowskiSystem) -> tuple[int, int, int] | None:
    """``(d_1, d_2, d_3)`` when every ``α_k`` is purely periodic of length 1."""
    coeffs = characteristic_poly_coeffs(system)
    if coeffs is None or system.order != 3:
        return None
    return (system.d(1, 1), system.d(2, 1), system.d(3, 1))


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


__all__ = [
    "constant_digits",
    "cubic_roots",
    "exact_pisot_cubic_certificate",
    "eval_monic_cubic",
    "monic_cubic_discriminant",
    "polynomial_is_irreducible_cubic",
    "spectral_data",
]
