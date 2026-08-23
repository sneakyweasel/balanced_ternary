"""Residual-state complexity of section jets.

For fixed ``f`` and depth ``k``, the raw state set is

    S_k(f) = { 𝔇_w f : |w| < k }.

Minimization identifies residuals that produce the same future output
trit stream on a bounded sample of residual arguments. This is
computational, not a closed-form state-count theorem.

Unbounded integer polynomial coefficients are not one FST; a *fixed*
``f`` at *fixed* ``k`` has a finite raw residual set of size at most
``(3^k - 1)/2``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from bt.calculus.jets import function_jet, integer_jet
from bt.calculus.section import IntPoly
from bt.representation import encode


def all_words(max_len: int) -> list[tuple[int, ...]]:
    if max_len < 0:
        raise ValueError("max_len must be >= 0")
    out: list[tuple[int, ...]] = [()]
    for k in range(1, max_len):
        for w in product((-1, 0, 1), repeat=k):
            out.append(w)
    return out


def residual_set(f: IntPoly, k: int) -> list[IntPoly]:
    """Raw residuals ``𝔇_w f`` for ``|w| < k``."""
    seen: dict[tuple[int, ...], IntPoly] = {}
    for w in all_words(k):
        jet = function_jet(f, w)
        seen[jet.residual().coeffs] = jet.residual()
    return list(seen.values())


def signature(poly: IntPoly, sample: range) -> tuple[int, ...]:
    """Output LSD of ``poly(x)`` on a sample — proxy for future output trit."""
    return tuple(int(encode(poly.eval(x)).digits_lsd()[0]) for x in sample)


def minimized_count(f: IntPoly, k: int, sample: range | None = None) -> int:
    sample = sample or range(-20, 21)
    sigs = {signature(p, sample) for p in residual_set(f, k)}
    return len(sigs)


@dataclass(frozen=True)
class JetProfile:
    poly: str
    depth: int
    raw_states: int
    minimized_states: int
    max_coeff: int
    max_degree: int
    lc_abs: int

    def as_dict(self) -> dict[str, object]:
        return {
            "poly": self.poly,
            "depth": self.depth,
            "raw_states": self.raw_states,
            "minimized_states": self.minimized_states,
            "max_coeff": self.max_coeff,
            "max_degree": self.max_degree,
            "lc_abs": self.lc_abs,
        }


def profile_jet(f: IntPoly, k: int) -> JetProfile:
    states = residual_set(f, k)
    max_c = max((max(abs(c) for c in p.coeffs) for p in states), default=0)
    max_d = max((p.degree for p in states), default=-1)
    lc = max((abs(p.lc()) for p in states if p.degree >= 0), default=0)
    return JetProfile(
        poly=f.render(),
        depth=k,
        raw_states=len(states),
        minimized_states=minimized_count(f, k),
        max_coeff=max_c,
        max_degree=max_d,
        lc_abs=lc,
    )


STANDARD_PROFILES: tuple[tuple[str, IntPoly], ...] = (
    ("x", IntPoly((0, 1))),
    ("x+1", IntPoly((1, 1))),
    ("2x+1", IntPoly((1, 2))),
    ("3x+1", IntPoly((1, 3))),
    ("x^2", IntPoly((0, 0, 1))),
    ("x^3", IntPoly((0, 0, 0, 1))),
    ("x^4", IntPoly((0, 0, 0, 0, 1))),
    ("ax+b", IntPoly((2, -3))),
)


def profile_standard(k: int = 3) -> list[JetProfile]:
    return [profile_jet(p, k) for _name, p in STANDARD_PROFILES]


def same_index_locality(f: IntPoly, n: int, k: int) -> bool:
    """Output trit ``i`` equals a function of input trit ``i`` alone.

    False as soon as two integers with the same ``a_i`` but different
    prefixes produce different output trits at ``i``.
    """
    a_i = integer_jet(n, k)[-1] if k else 0
    out_i = integer_jet(f.eval(n), k)[-1] if k else 0
    for m in range(-40, 41):
        w = integer_jet(m, k)
        if not w:
            continue
        if w[-1] != a_i:
            continue
        ow = integer_jet(f.eval(m), k)
        if ow[-1] != out_i:
            return False
    return True
