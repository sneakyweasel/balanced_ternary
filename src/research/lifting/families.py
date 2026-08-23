"""Test polynomials for 3-adic lifting experiments.

The families are chosen so that the derivative behaviour is controlled
rather than incidental:

* ``x^3 - x - c`` has ``f' = 3x^2 - 1``, a unit at every integer, so every
  node is nonsingular and ordinary Hensel uniqueness must appear;
* ``x^3 - c`` has ``f' = 3x^2``, divisible by 3 at every integer, so every
  node is singular;
* ``x^2 - c`` and ``x^4 - c`` are singular exactly on ``x = 0 (mod 3)``,
  giving mixed trees;
* ``x^3 - x`` vanishes modulo 3 as a function (Fermat), so the root splits
  three ways before any lifting decision is made;
* ``3(x^3 - x)`` vanishes modulo 9 as a function, giving a two-level
  pre-lifting tail where every residue survives.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.section import IntPoly, parse_poly


@dataclass(frozen=True)
class Family:
    """One named test polynomial with the reason it is in the set."""

    id: str
    poly: IntPoly
    note: str

    def as_dict(self) -> dict[str, object]:
        return {"id": self.id, "poly": self.poly.render(), "note": self.note}


SMALL_C: tuple[int, ...] = (0, 1, 2, 3, 4, 6, 8, 9, 27, -1, -3, -9)


def _const_suffix(c: int) -> str:
    if c == 0:
        return ""
    return f"-{c}" if c > 0 else f"+{-c}"


def _pure_power(degree: int) -> tuple[Family, ...]:
    if degree % 2 == 1:
        note = f"f' = {degree}x^{degree - 1} is divisible by 3 everywhere: every node is singular"
    else:
        note = f"f' = {degree}x^{degree - 1}: singular exactly on x = 0 (mod 3)"
    return tuple(
        Family(
            id=f"x^{degree}{_const_suffix(c)}",
            poly=IntPoly.from_dict({degree: 1, 0: -c}),
            note=note,
        )
        for c in SMALL_C
    )


def _depressed_cubic() -> tuple[Family, ...]:
    return tuple(
        Family(
            id=f"x^3-x{_const_suffix(c)}",
            poly=IntPoly.from_dict({3: 1, 1: -1, 0: -c}),
            note="f' = 3x^2 - 1 is a unit everywhere: purely nonsingular",
        )
        for c in SMALL_C
    )


SPECIAL: tuple[Family, ...] = (
    Family(
        id="x^3-x",
        poly=parse_poly("x^3-x"),
        note="vanishes mod 3 as a function; root splits three ways, then unique lifts",
    ),
    Family(
        id="3x^3-3x",
        poly=parse_poly("3x^3-3x"),
        note="vanishes mod 9 as a function; two-level pre-lifting tail",
    ),
    Family(
        id="9x^3-9x",
        poly=parse_poly("9x^3-9x"),
        note="vanishes mod 27 as a function; three-level pre-lifting tail",
    ),
    Family(
        id="x^2-3",
        poly=parse_poly("x^2-3"),
        note="f(0) = f'(0) = 0 (mod 3); singular root that dies at level 2",
    ),
    Family(
        id="x^3-3",
        poly=parse_poly("x^3-3"),
        note="f(0) = f'(0) = 0 (mod 3) and f' singular everywhere",
    ),
    Family(
        id="x^2-9",
        poly=parse_poly("x^2-9"),
        note="singular root that does lift, with a delayed split",
    ),
    Family(
        id="x^4-x^2",
        poly=parse_poly("x^4-x^2"),
        note="repeated factor x^2(x-1)(x+1): merging and splitting branches",
    ),
    Family(
        id="x^3+3x",
        poly=parse_poly("x^3+3x"),
        note="singular derivative with a nonzero linear term",
    ),
    Family(
        id="2x^4-x^2+5",
        poly=parse_poly("2x^4-x^2+5"),
        note="generic quartic control with a non-unit leading coefficient",
    ),
)


def all_families() -> tuple[Family, ...]:
    """Every named test polynomial, deduplicated by rendered form.

    ``SPECIAL`` comes first so the hand-written ids win over the
    systematic ones when two entries denote the same polynomial.
    """
    seen: dict[str, Family] = {}
    for fam in SPECIAL + _pure_power(2) + _pure_power(3) + _pure_power(4) + _depressed_cubic():
        seen.setdefault(fam.poly.render(), fam)
    return tuple(seen.values())


def all_polys() -> tuple[IntPoly, ...]:
    """Polynomials of :func:`all_families`."""
    return tuple(fam.poly for fam in all_families())


def family(family_id: str) -> Family:
    for fam in all_families():
        if fam.id == family_id:
            return fam
    raise KeyError(family_id)


NONSINGULAR_IDS: tuple[str, ...] = ("x^3-x", "x^3-x-1", "x^3-x-2", "x^3-x-3")
SINGULAR_IDS: tuple[str, ...] = ("x^3-3", "x^3-9", "x^2-3", "x^2-9", "x^3+3x")
