"""Integer jets and function-side residual section jets.

Integer jet (existing object, kept):

    J_k(n) = (lsd(n), lsd(D(n)), ..., lsd(D^{k-1}(n)))

Function jet along a section word ``w = a0...a_{k-1}``:

    f_ε = f
    f_{wa} = 𝔇_a(f_w)
    b_i = ρ_{a_i}(f_{a0...a_{i-1}})

This is a path of residual polynomials, not a classical Taylor jet.
Reconstruction:

    f(n) = b0 + 3 b1 + ... + 3^{k-1} b_{k-1} + 3^k f_w(D^k(n))
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.derivative import D, D_k, digit_at, lsd
from bt.calculus.section import IntPoly
from bt.representation import encode


def integer_jet(n: int, k: int) -> tuple[int, ...]:
    if k < 0:
        raise ValueError("k must be >= 0")
    return tuple(int(digit_at(n, i)) for i in range(k))


def residual_argument(n: int, k: int) -> int:
    return D_k(n, k)


@dataclass(frozen=True)
class FunctionJet:
    poly: IntPoly
    word: tuple[int, ...]
    residuals: tuple[IntPoly, ...]
    output_trits: tuple[int, ...]

    def residual(self) -> IntPoly:
        return self.residuals[-1]

    def as_dict(self) -> dict[str, object]:
        return {
            "poly": self.poly.render(),
            "word": list(self.word),
            "output_trits": list(self.output_trits),
            "residuals": [r.render() for r in self.residuals],
        }


def function_jet(f: IntPoly, word: tuple[int, ...]) -> FunctionJet:
    """Residual path of ``f`` along a trit section word."""
    for a in word:
        if a not in (-1, 0, 1):
            raise ValueError(f"section word must be trits, got {a}")
    residuals = [f]
    bits: list[int] = []
    cur = f
    for a in word:
        bits.append(cur.rho(a))
        cur = cur.section_deriv(a)
        residuals.append(cur)
    return FunctionJet(
        poly=f,
        word=word,
        residuals=tuple(residuals),
        output_trits=tuple(bits),
    )


def function_jet_of_integer(f: IntPoly, n: int, k: int) -> FunctionJet:
    """Section word = integer jet of ``n`` of length ``k``."""
    return function_jet(f, integer_jet(n, k))


def reconstruct_along_jet(jet: FunctionJet, residual_arg: int) -> int:
    acc = jet.residual().eval(residual_arg)
    for b in reversed(jet.output_trits):
        acc = b + 3 * acc
    return acc


def reconstruction_holds(f: IntPoly, n: int, k: int) -> bool:
    jet = function_jet_of_integer(f, n, k)
    return reconstruct_along_jet(jet, residual_argument(n, k)) == f.eval(n)


def output_prefix_depends_on_input_prefix(f: IntPoly, n: int, m: int, k: int) -> bool:
    """Low ``k`` output trits of ``f(n)`` vs ``f(m)`` when ``n ≡ m (mod 3^k)``.

    Balanced low digits determine ``n mod 3^k`` in the signed sense: equal
    integer jets of length ``k``.
    """
    if integer_jet(n, k) != integer_jet(m, k):
        return True
    fn = encode(f.eval(n)).digits_lsd()
    fm = encode(f.eval(m)).digits_lsd()
    a = (fn + (0,) * k)[:k]
    b = (fm + (0,) * k)[:k]
    return a == b
