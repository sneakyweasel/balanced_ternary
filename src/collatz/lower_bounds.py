"""Exploratory lower bounds on ``log R`` along valuation itineraries.

**PROVED.** ``1 <= R(ks) < 2^{K+1}``, so ``0 <= log2 R < K+1``. Nested
lifts satisfy ``R' = R + t * 2^{K+1}`` with integer ``t >= 0`` and
``t < 2^{j}`` when appending valuation ``j``. If ``t >= 1`` for infinitely
many prefixes of an infinite itinerary, then ``R_m -> infinity``.

No finite-state certificate of ``R_m -> infinity`` for a class of
non-contracting itineraries is claimed. Helpers below *search* for
``t = 0`` (R stays put) and for multiplicative jumps. Results are
**OBSERVATION** / **CONJECTURE** unless a proof is written.

Do not use machine learning. Do not treat a failed search as a theorem.
"""

from __future__ import annotations

from dataclasses import dataclass

from collatz.compatibility import child_realizer_delta
from collatz.cylinders import parse_ks
from collatz.min_realizer import min_realizer


def log2_R_upper_bound_exponent(ks: tuple[int, ...]) -> int:
    """``K+1``. **PROVED:** ``R < 2^{K+1}``."""
    ks = parse_ks(ks)
    return sum(ks) + 1


def lift_t(parent: tuple[int, ...], j: int) -> int:
    """The integer ``t`` in ``R_child = R_parent + t * 2^{K_parent+1}``."""
    _rp, _rc, t = child_realizer_delta(parent, j)
    return t


def search_zero_lifts(
    max_length: int, k_max: int
) -> tuple[tuple[tuple[int, ...], int], ...]:
    """Prefixes ``(parent, j)`` with ``t = 0`` (child R equals parent R)."""
    found: list[tuple[tuple[int, ...], int]] = []
    prefixes: list[tuple[int, ...]] = [()]
    for _ in range(max_length):
        nxt: list[tuple[int, ...]] = []
        for parent in prefixes:
            for j in range(1, k_max + 1):
                t = lift_t(parent, j)
                if t == 0:
                    found.append((parent, j))
                nxt.append(parent + (j,))
        prefixes = nxt
    return tuple(found)


def search_r_jumps(
    max_length: int, k_max: int, min_factor: int = 4
) -> tuple[dict[str, object], ...]:
    """Edges where ``R_child >= min_factor * R_parent`` (and parent R > 0)."""
    out: list[dict[str, object]] = []
    prefixes: list[tuple[int, ...]] = [()]
    for _ in range(max_length):
        nxt: list[tuple[int, ...]] = []
        for parent in prefixes:
            r_p = min_realizer(parent)
            for j in range(1, k_max + 1):
                r_c = min_realizer(parent + (j,))
                if r_p > 0 and r_c >= min_factor * r_p:
                    out.append(
                        {
                            "parent": list(parent),
                            "j": j,
                            "R_parent": r_p,
                            "R_child": r_c,
                            "status": "COMPUTATIONAL",
                        }
                    )
                nxt.append(parent + (j,))
        prefixes = nxt
    return tuple(out)


@dataclass(frozen=True)
class CertificateAttempt:
    name: str
    statement: str
    status: str
    evidence: str


def certificate_attempts() -> tuple[CertificateAttempt, ...]:
    """Formal statements. None is a Collatz theorem."""
    return (
        CertificateAttempt(
            name="trivial_upper_bound",
            statement="R(ks) < 2^{K+1}, so log2 R < K+1.",
            status="PROVED",
            evidence="R is the unique residue in (0, 2^{K+1}).",
        ),
        CertificateAttempt(
            name="nested_lift",
            statement="R' = R + t 2^{K+1} with t >= 0. Infinitely many t>=1 implies R_m -> inf.",
            status="PROVED",
            evidence="Nested cylinders at leftover Q=1.",
        ),
        CertificateAttempt(
            name="all_ones_R_unbounded",
            statement="R((1,)*m) = 2^{m+1}-1, hence R_m -> infinity.",
            status="PROVED",
            evidence="Induction on the inverse step: if r=2^P-1 then the k=1 preimage is 2^{P+1}-1.",
        ),
        CertificateAttempt(
            name="expansionary_forces_R_to_infinity",
            statement="If liminf K_m/m <= log2 3, then R_m -> infinity.",
            status="CONJECTURE",
            evidence="The exceptional itinerary compatibility problem. No certificate found.",
        ),
        CertificateAttempt(
            name="weighted_automaton_logR",
            statement="A finite weighted automaton computing a lower bound on log R that diverges on non-contracting paths.",
            status="OBSERVATION",
            evidence="Not constructed. The residue itself is already a 2-adic state of growing precision.",
        ),
    )
