"""Small, structurally varied polynomial families for dynamics triage."""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.section import IntPoly


@dataclass(frozen=True)
class DynamicsFamily:
    """One polynomial and its family label."""

    id: str
    poly: IntPoly
    family: str
    c: int


SMALL_C: tuple[int, ...] = (-3, -2, -1, 0, 1, 2, 3)


def _member(family: str, degree: int, c: int, *, linear: int = 0) -> DynamicsFamily:
    terms = {degree: 1, 0: c}
    if linear:
        terms[1] = linear
    suffix = f"+{c}" if c >= 0 else str(c)
    return DynamicsFamily(
        id=f"{family}{suffix}",
        poly=IntPoly.from_dict(terms),
        family=family,
        c=c,
    )


def all_families() -> tuple[DynamicsFamily, ...]:
    """The four prescribed families with small constants."""

    out: list[DynamicsFamily] = []
    for c in SMALL_C:
        out.extend(
            (
                _member("x^2", 2, c),
                _member("x^3", 3, c),
                _member("x^3-x", 3, c, linear=-1),
                _member("x^4", 4, c),
            )
        )
    return tuple(out)
