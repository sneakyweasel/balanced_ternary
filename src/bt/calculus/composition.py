"""Cascade composition of residual Mealy machines.

The section chain rule

    𝔇_a(f ∘ g) = 𝔇_{ρ_a(g)} f ∘ 𝔇_a g

is a cascade (not a synchronous product): the f-machine is driven by the
output trits of the g-machine. Naive state bound before minimization:

    M_k(f ∘ g) ≤ M_k(f) M_k(g)

in the remaining-depth unfolding, because a cascade state is a pair
(g-residual, f-residual along g's output). Minimization may reduce this.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.myhill_nerode import myhill_nerode_count
from bt.calculus.residual import delta, rho
from bt.calculus.section import IntPoly


def compose_neg(f: IntPoly) -> IntPoly:
    return f.compose(IntPoly((0, -1)))


def negation_rho_delta(f: IntPoly, a: int) -> bool:
    """``ρ_a(f ∘ N) = ρ_{-a}(f)`` and ``𝔇_a(f ∘ N) = (𝔇_{-a} f) ∘ N``."""
    fn = compose_neg(f)
    if rho(fn, a) != rho(f, -a):
        return False
    left = delta(fn, a)
    right = compose_neg(delta(f, -a))
    return left.coeffs == right.coeffs


def cascade_state_bound(f: IntPoly, g: IntPoly, k: int) -> int:
    return myhill_nerode_count(f, k) * myhill_nerode_count(g, k)


@dataclass(frozen=True)
class CompositionProfile:
    f: str
    g: str
    fog: str
    depth: int
    M_f: int
    M_g: int
    M_fog: int
    naive_product: int
    blowup: float | None

    def as_dict(self) -> dict[str, object]:
        return {
            "f": self.f,
            "g": self.g,
            "fog": self.fog,
            "depth": self.depth,
            "M_f": self.M_f,
            "M_g": self.M_g,
            "M_fog": self.M_fog,
            "naive_product": self.naive_product,
            "blowup": self.blowup,
        }


def profile_composition(f: IntPoly, g: IntPoly, k: int) -> CompositionProfile:
    fog = f.compose(g)
    mf = myhill_nerode_count(f, k)
    mg = myhill_nerode_count(g, k)
    mfg = myhill_nerode_count(fog, k)
    prod = mf * mg
    return CompositionProfile(
        f=f.render(),
        g=g.render(),
        fog=fog.render(),
        depth=k,
        M_f=mf,
        M_g=mg,
        M_fog=mfg,
        naive_product=prod,
        blowup=(mfg / prod) if prod else None,
    )


STANDARD_COMPOSITIONS: tuple[tuple[str, str], ...] = (
    ("x^2", "x^2"),
    ("x^2", "2x+1"),
    ("2x+1", "x^2"),
    ("x^3", "x+1"),
    ("x", "x^2"),
    ("x^2", "x"),
)


def profile_standard_compositions(k: int) -> list[CompositionProfile]:
    from bt.calculus.section import parse_poly

    rows = []
    for fs, gs in STANDARD_COMPOSITIONS:
        rows.append(profile_composition(parse_poly(fs), parse_poly(gs), k))
    return rows


def output_cascade_holds(f: IntPoly, g: IntPoly, word: tuple[int, ...]) -> bool:
    """``outputAlong(w, f∘g) = outputAlong(outputAlong(w, g), f)``."""
    from bt.calculus.residual import output_along

    fog = f.compose(g)
    return output_along(fog, word) == output_along(f, output_along(g, word))
