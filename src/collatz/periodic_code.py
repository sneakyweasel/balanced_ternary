"""Periodic valuation codes as candidate affine fixed points.

A period-``p`` word with affine data ``(C, K)`` can be a positive odd
cycle only if

    n (2^K - 3^p) = C

and ``n`` is a positive odd integer in the cylinder that actually repeats
the period. Expanding periods (``2^K < 3^p``) yield a negative candidate
because ``C > 0``. Equality ``2^K = 3^p`` is impossible for ``p >= 1``.

This module does not claim that excluding a periodic code proves Collatz.
"""

from __future__ import annotations

from dataclasses import dataclass

from collatz.itinerary import ValuationItinerary
from collatz.periodic_itineraries import PeriodicCandidate, periodic_candidate


def periodic_fixed_point_numerator(C: int, two_power: int, three_power: int) -> int:
    """Integer identity ``n (2^K - 3^p) - C`` vanishes at a period point."""
    return C  # used with gap; kept for the Lean/Python dictionary


def periodic_candidate_rational(valuations: tuple[int, ...]) -> PeriodicCandidate:
    """Exact candidate ``n = C / (2^K - 3^p)`` plus cylinder/orbit checks."""
    return periodic_candidate(valuations)


@dataclass(frozen=True)
class PeriodicFixedPointTheorem:
    """Record of the exact period-point identity for one code."""

    valuations: tuple[int, ...]
    p: int
    K: int
    C: int
    gap: int
    identity: str
    positive_candidate: int | None
    expanding_excludes_positive: bool
    status: str

    @classmethod
    def from_valuations(cls, valuations: tuple[int, ...]) -> "PeriodicFixedPointTheorem":
        itinerary = ValuationItinerary.from_ks(valuations)
        if itinerary.m < 1:
            raise ValueError("a period must be nonempty")
        gap = itinerary.denominator - itinerary.numerator_multiplier
        expanding = gap < 0
        candidate = None
        if gap > 0 and itinerary.C % gap == 0:
            value = itinerary.C // gap
            if value > 0:
                candidate = value
        return cls(
            valuations=tuple(valuations),
            p=itinerary.m,
            K=itinerary.K,
            C=itinerary.C,
            gap=gap,
            identity="n * (2^K - 3^p) = C",
            positive_candidate=candidate,
            expanding_excludes_positive=expanding,
            status="PROVED as an affine identity; cylinder membership is extra",
        )
