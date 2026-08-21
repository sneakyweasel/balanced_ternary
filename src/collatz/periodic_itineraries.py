"""Periodic and eventually periodic valuation itineraries.

If a period-``p`` word ``ks`` is realised by a positive odd cycle point,
the affine identity ``T^p(n)=n`` becomes

    n (2^K - 3^p) = C(ks),

so there is at most one candidate

    n = C / (2^K - 3^p)

when ``2^K > 3^p``. If ``2^K < 3^p`` the candidate is negative
(**PROVED**: ``C > 0`` for ``p > 0``), so an expanding periodic
itinerary has no positive integer realizer. Equality is impossible for
``p > 0``.

The candidate still has to lie in the cylinder and actually be a cycle.
That check is exact.

Eventually periodic ``u v^ω``: a realizer is a preimage of the cycle
point along ``u``, unique when it exists,

    n = (n_cycle * 2^{K_u} - C_u) / 3^{|u|}.

The 1-cycle ``(2)^ω`` with ``n=1`` is the unique positive cycle found
in the small search range. That is **VERIFIED COMPUTATIONALLY**, not a
proof that no other cycles exist (the Collatz cycle problem).
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from collatz.core import collatz_step
from collatz.cylinders import belongs_to_cylinder, parse_ks
from collatz.itinerary import ValuationItinerary, affine_constant


@dataclass(frozen=True)
class PeriodicCandidate:
    ks: tuple[int, ...]
    K: int
    p: int
    C: int
    gap: int  # 2^K - 3^p
    n: int | None
    compatible: bool
    reason: str
    status: str

    def as_dict(self) -> dict[str, object]:
        return {
            "ks": list(self.ks),
            "K": self.K,
            "p": self.p,
            "C": self.C,
            "gap": self.gap,
            "n": self.n,
            "compatible": self.compatible,
            "reason": self.reason,
            "status": self.status,
        }

    def format(self) -> str:
        return (
            f"Periodic itinerary  ks={self.ks}  p={self.p} K={self.K}\n"
            f"C={self.C}  2^K-3^p={self.gap}  n={self.n}\n"
            f"compatible={str(self.compatible).lower()}  {self.reason}\n"
            f"status: {self.status}\n"
        )


def periodic_candidate(ks: tuple[int, ...] | str | list[int]) -> PeriodicCandidate:
    ks = parse_ks(ks)
    if not ks:
        return PeriodicCandidate(
            ks=ks, K=0, p=0, C=0, gap=0, n=1,
            compatible=True,
            reason="empty period is the identity at every odd n; not a cycle test",
            status="EXACT",
        )
    it = ValuationItinerary.from_ks(ks)
    gap = it.denominator - it.numerator_multiplier
    status = "EXACT"
    if gap < 0:
        return PeriodicCandidate(
            ks=ks, K=it.K, p=it.m, C=it.C, gap=gap, n=None,
            compatible=False,
            reason="expanding period: C/(2^K-3^p) < 0, no positive realizer",
            status=status,
        )
    if gap == 0:
        return PeriodicCandidate(
            ks=ks, K=it.K, p=it.m, C=it.C, gap=gap, n=None,
            compatible=False,
            reason="2^K=3^p is impossible for m>0",
            status=status,
        )
    if it.C % gap != 0:
        return PeriodicCandidate(
            ks=ks, K=it.K, p=it.m, C=it.C, gap=gap, n=None,
            compatible=False,
            reason="C not divisible by 2^K-3^p",
            status=status,
        )
    n = it.C // gap
    if n <= 0 or n % 2 == 0:
        return PeriodicCandidate(
            ks=ks, K=it.K, p=it.m, C=it.C, gap=gap, n=n,
            compatible=False,
            reason="candidate is not a positive odd integer",
            status=status,
        )
    if not belongs_to_cylinder(n, ks):
        return PeriodicCandidate(
            ks=ks, K=it.K, p=it.m, C=it.C, gap=gap, n=n,
            compatible=False,
            reason="candidate not in the valuation cylinder",
            status=status,
        )
    x = n
    for _ in ks:
        x = collatz_step(x)
    if x != n:
        return PeriodicCandidate(
            ks=ks, K=it.K, p=it.m, C=it.C, gap=gap, n=n,
            compatible=False,
            reason="affine fixed point is not a T-cycle on this word",
            status=status,
        )
    return PeriodicCandidate(
        ks=ks, K=it.K, p=it.m, C=it.C, gap=gap, n=n,
        compatible=True,
        reason="positive odd cycle point",
        status=status,
    )


def preimage_along(
    prefix: tuple[int, ...], target: int
) -> int | None:
    """Unique affine preimage of ``target`` along ``prefix``, or ``None``."""
    prefix = parse_ks(prefix)
    if isinstance(target, bool) or not isinstance(target, int):
        raise TypeError("target must be int")
    it = ValuationItinerary.from_ks(prefix)
    num = target * it.denominator - it.C
    if num % it.numerator_multiplier != 0:
        return None
    n = num // it.numerator_multiplier
    if n <= 0 or n % 2 == 0:
        return None
    if not belongs_to_cylinder(n, prefix):
        return None
    if it.apply(n) != target:
        return None
    return n


def eventually_periodic_realizer(
    prefix: tuple[int, ...], cycle: tuple[int, ...]
) -> PeriodicCandidate:
    """Realizer of ``prefix + cycle^ω``, if the cycle has a positive point."""
    cyc = periodic_candidate(cycle)
    if not cyc.compatible or cyc.n is None:
        return PeriodicCandidate(
            ks=parse_ks(prefix) + parse_ks(cycle),
            K=sum(parse_ks(prefix)) + sum(parse_ks(cycle)),
            p=len(parse_ks(cycle)),
            C=affine_constant(parse_ks(prefix) + parse_ks(cycle)),
            gap=cyc.gap,
            n=None,
            compatible=False,
            reason=f"cycle not compatible: {cyc.reason}",
            status="EXACT",
        )
    prefix = parse_ks(prefix)
    n = preimage_along(prefix, cyc.n)
    if n is None:
        return PeriodicCandidate(
            ks=prefix + parse_ks(cycle),
            K=sum(prefix) + sum(parse_ks(cycle)),
            p=len(parse_ks(cycle)),
            C=affine_constant(prefix + parse_ks(cycle)),
            gap=cyc.gap,
            n=None,
            compatible=False,
            reason="no positive odd preimage of the cycle point along the prefix",
            status="EXACT",
        )
    return PeriodicCandidate(
        ks=prefix + parse_ks(cycle),
        K=sum(prefix) + cyc.K,
        p=cyc.p,
        C=affine_constant(prefix + parse_ks(cycle)),
        gap=cyc.gap,
        n=n,
        compatible=True,
        reason=f"preimage of cycle point {cyc.n} along prefix",
        status="EXACT",
    )


def search_periodic(max_length: int, k_max: int) -> tuple[PeriodicCandidate, ...]:
    """All compatible cycles with ``1 <= p <= max_length``, ``k_i <= k_max``."""
    if isinstance(max_length, bool) or not isinstance(max_length, int) or max_length < 1:
        raise ValueError(f"max_length must be an integer >= 1, got {max_length!r}")
    if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
        raise ValueError(f"k_max must be an integer >= 1, got {k_max!r}")
    found: list[PeriodicCandidate] = []
    for p in range(1, max_length + 1):
        for ks in product(range(1, k_max + 1), repeat=p):
            cand = periodic_candidate(ks)
            if cand.compatible:
                found.append(cand)
    return tuple(found)
