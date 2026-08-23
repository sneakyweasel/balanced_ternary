"""Closed form of quadratic residuals of ``x^2``.

Every residual along a trit word ``w`` (LSD-first) is

    f_w(x) = 3^{|w|} x^2 + 2 p(w) x + D^{|w|}(p(w)^2)

where ``p(w)`` is the packed prefix. Distinct prefixes give distinct
polynomials, and for degree ``≤ 2`` the Myhill–Nerode class at horizon
``k`` is exactly the triple ``(A, B, C) mod 3^k``.
"""

from __future__ import annotations

from itertools import product

from bt.calculus.residual import TRITS, delta, output_along, residual_along, rho
from bt.calculus.section import IntPoly
from bt.normtheory.rewrite import balanced_divmod


def pack_word(word: tuple[int, ...]) -> int:
    """LSD-first packed value ``Σ a_i 3^i``."""
    acc = 0
    pow3 = 1
    for a in word:
        acc += a * pow3
        pow3 *= 3
    return acc


def iter_dz(n: int, m: int) -> int:
    """``D`` iterated ``m`` times (balanced quotient)."""
    cur = n
    for _ in range(m):
        _r, cur = balanced_divmod(cur)
    return cur


def quad_poly(A: int, B: int, C: int) -> IntPoly:
    """``A x^2 + B x + C``, LSD-first coefficients."""
    return IntPoly((C, B, A))


def coeff_triple(f: IntPoly) -> tuple[int, int, int]:
    """``(A, B, C)`` of a degree-``≤ 2`` polynomial."""
    return (f.coefficient(2), f.coefficient(1), f.coefficient(0))


def quadratic_residual_formula(word: tuple[int, ...]) -> IntPoly:
    """Closed form of the residual of ``x^2`` along ``word``."""
    m = len(word)
    p = pack_word(word)
    return quad_poly(3**m, 2 * p, iter_dz(p * p, m))


def section_coeff_step(A: int, B: int, C: int, a: int) -> tuple[int, int, int]:
    """Coefficient recurrence of ``𝔇_a`` on ``A x^2 + B x + C``."""
    val = A * a * a + B * a + C
    _rho, q = balanced_divmod(val)
    return (3 * A, B + 2 * A * a, q)


def invariant_mod(f: IntPoly, k: int) -> tuple[int, int, int]:
    """``(A, B, C) mod 3^k`` in ``[0, 3^k)``."""
    if k < 0:
        raise ValueError("k must be >= 0")
    mod = 3**k if k else 1
    A, B, C = coeff_triple(f)
    return (A % mod, B % mod, C % mod)


def canonical_distinguishing_word(f: IntPoly, g: IntPoly, k: int) -> tuple[int, ...] | None:
    """One of ``0^k``, ``10^{k-1}``, ``(-1)0^{k-1}`` if they differ at horizon ``k``.

    For degree ``≤ 2`` this is complete: the three evaluations ``h(0)``,
    ``h(1)``, ``h(-1)`` recover whether ``3^k`` divides all of ``ΔA, ΔB, ΔC``.
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    if k == 0:
        return None
    candidates = (
        (0,) * k,
        (1,) + (0,) * (k - 1),
        (-1,) + (0,) * (k - 1),
    )
    for word in candidates:
        if output_along(f, word) != output_along(g, word):
            return word
    return None


def residual_formula_table(f: IntPoly, k: int) -> list[dict[str, object]]:
    """Residuals of ``f`` for every prefix of length ``< k``, with coefficients."""
    if k < 0:
        raise ValueError("k must be >= 0")
    rows: list[dict[str, object]] = []
    for length in range(k):
        for word in product(TRITS, repeat=length) if length else ((),):
            poly = residual_along(f, word)
            A, B, C = coeff_triple(poly)
            closed = poly.coeffs == quadratic_residual_formula(word).coeffs
            packed = pack_word(word)
            rows.append(
                {
                    "word": list(word),
                    "pack": packed,
                    "pack": packed,
                    "poly": poly.render(),
                    "A": A,
                    "B": B,
                    "C": C,
                    "closed_x2": closed,
                    "closed_x2": closed,
                }
            )
    return rows


def rho_triples(f: IntPoly, k: int) -> set[tuple[int, int, int]]:
    """Immediate ``(ρ_{-1}, ρ_0, ρ_1)`` vectors of residuals with ``|w| < k``."""
    from bt.calculus.myhill_nerode import all_reachable

    out: set[tuple[int, int, int]] = set()
    for poly in all_reachable(f, max(k - 1, 0)):
        out.add((rho(poly, -1), rho(poly, 0), rho(poly, 1)))
    return out


def residuals_with_words(f: IntPoly, max_len: int) -> dict[tuple[int, ...], tuple[IntPoly, tuple[int, ...]]]:
    """First-seen residual polynomials with a generating word of length ``≤ max_len``."""
    if max_len < 0:
        raise ValueError("max_len must be >= 0")
    found: dict[tuple[int, ...], tuple[IntPoly, tuple[int, ...]]] = {f.coeffs: (f, ())}
    frontier: list[tuple[IntPoly, tuple[int, ...]]] = [(f, ())]
    for _ in range(max_len):
        nxt: list[tuple[IntPoly, tuple[int, ...]]] = []
        for poly, word in frontier:
            for a in TRITS:
                child = delta(poly, a)
                if child.coeffs not in found:
                    nw = word + (a,)
                    found[child.coeffs] = (child, nw)
                    nxt.append((child, nw))
        frontier = nxt
    return found
