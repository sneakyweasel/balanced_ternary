"""Nested cylinders versus ordinary positive integers.

Terminology (do not conflate):

- **FINITELY 2-ADICALLY REALIZABLE:** every finite prefix has a nonempty
  cylinder. **PROVED** in Milestone 3 for every word over ``{1,2,...}``.
- **2-ADICALLY REALIZABLE:** the nested cylinders have nonempty
  intersection in the odd 2-adics. Compactness of ``Z_2`` gives this for
  every infinite valuation sequence.
- **REALIZED BY A POSITIVE INTEGER:** some positive odd ``n`` lies in
  every finite cylinder of the sequence, i.e. realises the entire
  infinite itinerary.
- **REALIZED BY A POSITIVE INFINITE COLLATZ TRAJECTORY:** the same, and
  the forward orbit of that ``n`` is the usual accelerated Collatz orbit.

**PROPOSITION (nested realizers).** Let ``k_0, k_1, ...`` be an infinite
valuation sequence and ``R_m = R(k_0,...,k_{m-1})``. If a positive odd
integer ``n`` realises every finite prefix, then ``n >= R_m`` for all
``m``. Consequently, if ``R_m -> infinity``, no finite positive integer
realises the entire infinite itinerary.

This is a statement about a *prescribed* itinerary, not about arbitrary
Collatz trajectories, and not a proof of Collatz.

**PROVED:** ``R`` is nondecreasing on nested prefixes (see
``min_realizer``). Searching for a child with smaller ``R`` is a
regression test of that proof, not an open search.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from collatz.cylinders import parse_ks
from collatz.min_realizer import min_realizer, nested_realizers


class RealizabilityClass(str, Enum):
    FINITELY_TWO_ADICALLY_REALIZABLE = "FINITELY_2-ADICALLY_REALIZABLE"
    TWO_ADICALLY_REALIZABLE = "2-ADICALLY_REALIZABLE"
    REALIZED_BY_A_POSITIVE_INTEGER = "REALIZED_BY_A_POSITIVE_INTEGER"
    REALIZED_BY_A_POSITIVE_INFINITE_TRAJECTORY = (
        "REALIZED_BY_A_POSITIVE_INFINITE_COLLATZ_TRAJECTORY"
    )


def r_unbounded_excludes_positive_integer(r_seq: tuple[int, ...]) -> bool:
    """Finite check of the hypothesis ``R_m`` unbounded on a prefix sequence.

    Returns True if the observed prefix of ``R_m`` is strictly eventually
    increasing without a bound visible in the sample. This is **not** a
    proof that the infinite sequence is unbounded; it is the finite
    observation used by searches. The implication
    ``R_m -> inf => no positive integer realises the itinerary`` is
    **PROVED** and does not depend on this helper.
    """
    if len(r_seq) < 2:
        return False
    return r_seq[-1] > r_seq[0] and r_seq == tuple(sorted(r_seq))


def positive_integer_would_bound_R(n: int, r_seq: tuple[int, ...]) -> bool:
    """If ``n`` realises every prefix, then ``n >= max R_m``."""
    if not r_seq:
        return n >= 1
    return n >= max(r_seq)


@dataclass(frozen=True)
class NestedCylinderReport:
    ks: tuple[int, ...]
    realizers: tuple[int, ...]
    monotone: bool
    strictly_increasing: bool
    bounded_in_sample: bool
    class_labels: tuple[str, ...]
    status: str

    def format(self) -> str:
        return (
            f"Nested cylinders  ks={self.ks}\n"
            f"R_m={self.realizers}\n"
            f"monotone={str(self.monotone).lower()}  "
            f"[PROVED for leftover Q=1]\n"
            f"strictly_increasing={str(self.strictly_increasing).lower()}  "
            f"[COMPUTATIONAL on this prefix]\n"
            f"bounded_in_sample={str(self.bounded_in_sample).lower()}\n"
            f"classes: {', '.join(self.class_labels)}\n"
            f"status: {self.status}\n"
            "If R_m -> infinity, no finite positive integer realises the "
            "entire infinite itinerary. [PROVED]\n"
        )


def nested_cylinder_report(ks: tuple[int, ...] | str | list[int]) -> NestedCylinderReport:
    ks = parse_ks(ks)
    rs = nested_realizers(ks)
    monotone = all(rs[i] <= rs[i + 1] for i in range(len(rs) - 1))
    strict = all(rs[i] < rs[i + 1] for i in range(len(rs) - 1)) if len(rs) > 1 else False
    bounded = len(rs) >= 2 and rs[-1] == rs[0]
    labels = (
        RealizabilityClass.FINITELY_TWO_ADICALLY_REALIZABLE.value,
        RealizabilityClass.TWO_ADICALLY_REALIZABLE.value,
    )
    return NestedCylinderReport(
        ks=ks,
        realizers=rs,
        monotone=monotone,
        strictly_increasing=strict,
        bounded_in_sample=bounded,
        class_labels=labels,
        status="EXACT residues; COMPUTATIONAL boundedness on this finite prefix",
    )


def child_realizer_delta(parent: tuple[int, ...], j: int) -> tuple[int, int, int]:
    """Return ``(R_parent, R_child, t)`` with ``R_child = R_parent + t * 2^{K_p+1}``."""
    parent = parse_ks(parent)
    if isinstance(j, bool) or not isinstance(j, int) or j < 1:
        raise ValueError(f"j must be an integer >= 1, got {j!r}")
    r_p = min_realizer(parent)
    r_c = min_realizer(parent + (j,))
    mod = 1 << (sum(parent) + 1)
    if (r_c - r_p) % mod != 0:
        raise ArithmeticError("child residue does not lift the parent")
    t = (r_c - r_p) // mod
    return r_p, r_c, t
