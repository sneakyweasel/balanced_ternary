"""Constant-coefficient place-value recurrence as a ``RecurrenceSpec``.

Energy, live sets, and the recurrence word ``B*`` stay elsewhere.
"""

from __future__ import annotations

from research.ostrowski.system import OstrowskiSystem, characteristic_poly_coeffs
from research_engine.algebra.recurrences import RecurrenceSpec


def recurrence_spec(system: OstrowskiSystem) -> RecurrenceSpec | None:
    poly = characteristic_poly_coeffs(system)
    if poly is None:
        return None
    digits = tuple(-c for c in poly[1:])
    return RecurrenceSpec(coefficients=digits, initial_values=(1,))


def place_values_from_recurrence(system: OstrowskiSystem, n: int) -> tuple[int, ...] | None:
    spec = recurrence_spec(system)
    if spec is None:
        return None
    return spec.sequence(n)


def recurrence_matches_place_values(system: OstrowskiSystem, n: int) -> bool:
    computed = place_values_from_recurrence(system, n)
    if computed is None:
        return False
    return computed == system.place_values(n)


def companion_matches_residual(system: OstrowskiSystem) -> bool:
    from research.ostrowski.spectral_residual import residual_matrix

    spec = recurrence_spec(system)
    if spec is None:
        return False
    return spec.companion_matrix() == residual_matrix(system) and (
        spec.characteristic_polynomial() == characteristic_poly_coeffs(system)
    )
