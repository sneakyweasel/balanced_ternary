"""Kramer's exact 3-adic endpoint representative.

For a valuation prefix of length ``m``, total exponent ``K`` and affine
constant ``C``, Kramer uses the least-positive representative

    M = C * 2^(-K) (mod 3^m).

The empty prefix is assigned ``M = 1`` explicitly.  The modulus here is
``3^m``; no parity-refining factor of two is added.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, log1p

from collatz.cylinders import parse_ks
from collatz.itinerary import ValuationItinerary


def _require_length(m: int) -> int:
    if isinstance(m, bool) or not isinstance(m, int) or m < 0:
        raise ValueError("m must be an integer >= 0")
    return m


def real_drift(K: int, m: int) -> float:
    """Kramer's floating drift ``|K/m - log_2(3)|``.

    The empty-prefix value is defined as zero.  Exact drift comparisons should
    use the integer powers ``3**m`` and ``2**K`` instead.
    """
    m = _require_length(m)
    if isinstance(K, bool) or not isinstance(K, int) or K < 0:
        raise ValueError("K must be an integer >= 0")
    if m == 0:
        if K != 0:
            raise ValueError("the empty prefix must have K=0")
        return 0.0
    return abs(K / m - log(3) / log(2))


def start_residue_rate(r: int, m: int) -> float:
    """Natural-log rate ``ln(1+r)/m``, with empty value zero."""
    m = _require_length(m)
    if isinstance(r, bool) or not isinstance(r, int) or r < 0:
        raise ValueError("r must be a nonnegative integer")
    if m == 0:
        if r != 0:
            raise ValueError("the empty-prefix start residue must be zero")
        return 0.0
    return log1p(r) / m


def endpoint_residue_rate(M: int, m: int) -> float:
    """Natural-log rate ``ln(1 + M/(3/2)^m)/m``.

    The logarithm is evaluated stably for large exact integer representatives.
    """
    m = _require_length(m)
    if isinstance(M, bool) or not isinstance(M, int) or M < 1:
        raise ValueError("M must be a positive integer")
    if m == 0:
        if M != 1:
            raise ValueError("the empty-prefix endpoint representative must be one")
        return 0.0
    scaled_log = log(M) + m * (log(2) - log(3))
    if scaled_log > 0.0:
        value = scaled_log + log1p(exp(-scaled_log))
    else:
        value = log1p(exp(scaled_log))
    return value / m


def least_positive_residue(value: int, modulus: int) -> int:
    """Return the unique representative in ``1..modulus``.

    This differs from Python's ``%`` only when the residue is zero.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an int")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 1:
        raise ValueError("modulus must be an integer >= 1")
    residue = value % modulus
    return modulus if residue == 0 else residue


def kramer_endpoint_residue(
    valuations: tuple[int, ...] | list[int] | str,
) -> int:
    """Compute Kramer's ``M`` directly from the exact affine data."""
    ks = parse_ks(valuations)
    if not ks:
        return 1
    itinerary = ValuationItinerary.from_ks(ks)
    modulus = itinerary.numerator_multiplier
    inverse_two_K = pow(itinerary.denominator, -1, modulus)
    return least_positive_residue(itinerary.C * inverse_two_K, modulus)


def endpoint_congruence_holds(
    endpoint: int,
    valuations: tuple[int, ...] | list[int] | str,
) -> bool:
    """Whether ``endpoint == M (mod 3^m)`` under Kramer's convention."""
    if isinstance(endpoint, bool) or not isinstance(endpoint, int):
        return False
    ks = parse_ks(valuations)
    modulus = 3 ** len(ks)
    return endpoint % modulus == kramer_endpoint_residue(ks) % modulus


@dataclass(frozen=True)
class KramerEndpoint:
    """Exact data behind one 3-adic endpoint representative."""

    valuations: tuple[int, ...]
    m: int
    K: int
    C: int
    modulus: int
    M: int

    @classmethod
    def from_valuations(
        cls, valuations: tuple[int, ...] | list[int] | str
    ) -> "KramerEndpoint":
        ks = parse_ks(valuations)
        itinerary = ValuationItinerary.from_ks(ks)
        modulus = itinerary.numerator_multiplier
        endpoint = cls(
            valuations=ks,
            m=itinerary.m,
            K=itinerary.K,
            C=itinerary.C,
            modulus=modulus,
            M=kramer_endpoint_residue(ks),
        )
        if not endpoint.validates():
            raise ArithmeticError("Kramer endpoint construction failed validation")
        return endpoint

    def validates(self) -> bool:
        try:
            itinerary = ValuationItinerary.from_ks(self.valuations)
        except (TypeError, ValueError):
            return False
        if (
            self.m != itinerary.m
            or self.K != itinerary.K
            or self.C != itinerary.C
            or self.modulus != itinerary.numerator_multiplier
        ):
            return False
        if self.modulus != 3**self.m:
            return False
        if not 1 <= self.M <= self.modulus:
            return False
        if self.m == 0:
            return self.K == 0 and self.C == 0 and self.M == 1
        return (
            self.M % self.modulus
            == self.C * pow(1 << self.K, -1, self.modulus) % self.modulus
        )

    def contains(self, endpoint: int) -> bool:
        return endpoint_congruence_holds(endpoint, self.valuations)

    def as_dict(self) -> dict[str, object]:
        return {
            "valuations": list(self.valuations),
            "m": self.m,
            "K": self.K,
            "C": self.C,
            "modulus": self.modulus,
            "M": self.M,
            "representative": "least-positive",
            "status": "EXACT",
        }


# Short literature-facing spelling.
kramer_M = kramer_endpoint_residue
