"""Polynomial function congruence modulo ``3^k``.

Finite-horizon residual equivalence of ordinary ``Z[x]`` polynomials is
function congruence:

    f ≡_k g  iff  3^k | (f-g)(n)  for every integer n.

The kernel

    I_k = { h ∈ Z[x] : h(n) ≡ 0 (mod 3^k) for all n }

is **not** ``3^k Z[x]``. It is the set of polynomials whose Newton /
binomial coefficients ``Δ^j h(0)`` are all divisible by ``3^k``. This is
the classical characterization of polynomial functions on ``Z/nZ``
(Kempner; integer-valued polynomials), used here as the Myhill–Nerode
invariant of residual states.

Degree ``≤ 2`` is the baseline: ``2`` is a unit modulo ``3^k``, so
binomial residues recover monomial coefficients. Degree ``≥ 3`` admits
invisible polynomials such as ``x^3 - x`` modulo ``3``.
"""

from __future__ import annotations

from itertools import product
from math import comb, factorial

from bt.calculus.quadratic import iter_dz
from bt.calculus.section import IntPoly
from bt.metrics import v3


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def v3_finite(n: int) -> int | None:
    """``v_3(n)``, or ``None`` for ``n = 0``."""
    return v3(n)


def valuation_profile(coeffs: tuple[int, ...] | list[int]) -> list[int | None]:
    """Coefficientwise ``v_3`` of an LSD-first coefficient tuple."""
    return [v3(c) for c in coeffs]


def forward_difference(values: list[int]) -> list[int]:
    """One forward difference of a value table."""
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


def newton_coeffs(f: IntPoly) -> tuple[int, ...]:
    """Binomial / Newton coefficients ``a_j = Δ^j f(0)``.

    Then ``f(x) = Σ_j a_j binom(x, j)`` as functions on ``Z``.
    """
    if f.degree < 0:
        return (0,)
    table = [f.eval(i) for i in range(f.degree + 1)]
    out: list[int] = []
    for _ in range(f.degree + 1):
        out.append(table[0])
        table = forward_difference(table)
    return tuple(out)


def finite_difference_profile(f: IntPoly) -> tuple[int, ...]:
    """Alias of :func:`newton_coeffs`."""
    return newton_coeffs(f)


def residual_shift(f: IntPoly, m: int, p: int) -> IntPoly:
    """Binomial closed form of ``D^m(f(p + 3^m x))``.

    Lean name: ``residualShift``. The evaluation identity
    ``eval x (residualAlong w f) = D^{|w|}(f(packWord w + 3^{|w|} x))``
    is ``eval_residualAlong``.
    """
    m = _require_nat(m, "m")
    if f.degree < 0:
        return IntPoly((0,))
    out = [0] * (f.degree + 1)
    out[0] = iter_dz(f.eval(p), m)
    for j in range(1, f.degree + 1):
        acc = 0
        for n in range(j, f.degree + 1):
            a = f.coefficient(n)
            if a:
                acc += a * comb(n, j) * (p ** (n - j)) * (3 ** (m * (j - 1)))
        out[j] = acc
    return IntPoly(tuple(out))


def phi_k(f: IntPoly, k: int) -> tuple[int, ...]:
    """Canonical finite invariant: Newton residues modulo ``3^k``.

    ``f ≡_k g`` iff ``phi_k(f) = phi_k(g)`` after padding the shorter
    tuple by zeros. For a known degree bound ``d`` only ``d + 1``
    residues are required.
    """
    k = _require_nat(k, "k")
    mod = 3**k if k else 1
    return tuple(a % mod for a in newton_coeffs(f))


def pad_phi(phi: tuple[int, ...], length: int) -> tuple[int, ...]:
    """Pad Newton residues by zeros (higher differences of lower degree)."""
    if length < len(phi):
        raise ValueError("cannot truncate a Newton residue tuple")
    return phi + (0,) * (length - len(phi))


def phi_equal(f: IntPoly, g: IntPoly, k: int) -> bool:
    """Compare ``Φ_k`` after aligning degrees by zero-padding."""
    a, b = phi_k(f, k), phi_k(g, k)
    n = max(len(a), len(b))
    return pad_phi(a, n) == pad_phi(b, n)


def value_probes(f: IntPoly, points: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    """Evaluations of ``f`` at the given integer probes."""
    return tuple(f.eval(x) for x in points)


def probe_set(degree: int) -> tuple[int, ...]:
    """``0, 1, …, d``. Complete for degree ``≤ d`` via Newton interpolation."""
    degree = max(degree, 0)
    return tuple(range(degree + 1))


def balanced_probe_set(degree: int) -> tuple[int, ...]:
    """Balanced window of length ``d + 1`` centered at ``0``."""
    degree = max(degree, 0)
    lo = -((degree) // 2)
    return tuple(range(lo, lo + degree + 1))


def vanishes_as_function(f: IntPoly, k: int) -> bool:
    """``3^k | f(n)`` for every integer ``n``."""
    k = _require_nat(k, "k")
    if k == 0:
        return True
    mod = 3**k
    return all(a % mod == 0 for a in newton_coeffs(f))


def coeffwise_vanishes(f: IntPoly, k: int) -> bool:
    """``3^k`` divides every monomial coefficient."""
    k = _require_nat(k, "k")
    if k == 0:
        return True
    mod = 3**k
    return all(c % mod == 0 for c in f.coeffs)


def function_equiv(f: IntPoly, g: IntPoly, k: int) -> bool:
    """``f ≡_k g`` as polynomial functions modulo ``3^k``."""
    return vanishes_as_function(f.sub(g), k)


def distinguishing_residue(f: IntPoly, g: IntPoly, k: int) -> int | None:
    """Smallest-absolute-value residue at which ``f`` and ``g`` differ mod ``3^k``.

    Among equal absolute values, nonnegative residues are preferred.
    For degree ``d`` it is enough to search ``{-d,…,d}``; the search is
    therefore finite.
    """
    k = _require_nat(k, "k")
    if function_equiv(f, g, k):
        return None
    if k == 0:
        return None
    mod = 3**k
    h = f.sub(g)
    bound = max(h.degree, 0)
    candidates = [0]
    for i in range(1, bound + 1):
        candidates.append(i)
        candidates.append(-i)
    for x in candidates:
        if h.eval(x) % mod != 0:
            return x
    # Newton completeness: should be unreachable if the degree bound is correct.
    raise RuntimeError("function difference evaded the Newton probe window")


def first_distinction_horizon(f: IntPoly, g: IntPoly) -> int | None:
    """``τ(f, g) = min { k : f ≢_k g }``, or ``None`` if ``f = g``.

    Exact formula: if ``h = f - g ≠ 0`` and ``v = min_j v_3(Δ^j h(0))``,
    then ``τ = v + 1``. Distinct ordinary polynomials always have finite
    ``τ``.
    """
    h = f.sub(g)
    if h.coeffs == (0,):
        return None
    vals = [v3(a) for a in newton_coeffs(h)]
    finite = [v for v in vals if v is not None]
    return min(finite) + 1


def newton_valuation(f: IntPoly) -> int | None:
    """``min_j v_3(Δ^j f(0))``, or ``None`` if ``f = 0``."""
    if f.coeffs == (0,):
        return None
    vals = [v3(a) for a in newton_coeffs(f)]
    finite = [v for v in vals if v is not None]
    return min(finite) if finite else None


def monomial_valuation(f: IntPoly) -> int | None:
    """``min_j v_3(c_j)``, or ``None`` if ``f = 0``."""
    if f.coeffs == (0,):
        return None
    vals = [v3(c) for c in f.coeffs]
    finite = [v for v in vals if v is not None]
    return min(finite) if finite else None


def v3_factorial(n: int) -> int:
    """``v_3(n!)`` by de Polignac / Legendre."""
    n = _require_nat(n, "n")
    v = 0
    p = 3
    while p <= n:
        v += n // p
        p *= 3
    return v


def tau_leading_bound(h: IntPoly) -> int | None:
    """``τ ≤ 1 + v_3(d!) + v_3(lc(h))`` for nonzero ``h`` of degree ``d``."""
    if h.coeffs == (0,):
        return None
    d = h.degree
    lc_v = v3(h.lc())
    assert lc_v is not None
    return 1 + v3_factorial(d) + lc_v


def falling_factorial(j: int) -> IntPoly:
    """``x^{underline j} = x(x-1)…(x-j+1)``."""
    j = _require_nat(j, "j")
    acc = IntPoly((1,))
    x = IntPoly.X()
    for i in range(j):
        acc = acc.mul(x.sub(IntPoly.C(i)))
    return acc


def from_falling(b: tuple[int, ...] | list[int]) -> IntPoly:
    """``Σ b_j x^{underline j}``."""
    acc = IntPoly((0,))
    for j, coeff in enumerate(b):
        if coeff:
            acc = acc.add(falling_factorial(j).scale(coeff))
    return acc


def cubic_conditions(A: int, B: int, C: int, D: int, k: int) -> dict[str, bool]:
    """Exact degree-3 vanishing conditions modulo ``3^k``."""
    k = _require_nat(k, "k")
    mod = 3**k if k else 1
    return {
        "D": D % mod == 0,
        "A+B+C": (A + B + C) % mod == 0,
        "3A+B": (3 * A + B) % mod == 0,
        "6A": (6 * A) % mod == 0,
    }


def cubic_vanishes(A: int, B: int, C: int, D: int, k: int) -> bool:
    """``A x^3 + B x^2 + C x + D`` vanishes as a function modulo ``3^k``."""
    return all(cubic_conditions(A, B, C, D, k).values())


def _score(poly: IntPoly) -> tuple[int, int, int, tuple[int, ...]]:
    coeffs = poly.coeffs
    return (poly.degree, max(abs(c) for c in coeffs), sum(abs(c) for c in coeffs), coeffs)


def vanishing_poly(degree: int, k: int, *, box: int | None = None) -> dict[str, object]:
    """Search for vanishing polynomials of degree at most ``degree``.

    Returns the smallest coefficientwise kernel element (always ``3^k``
    for ``k ≥ 0``) and, when it exists, the smallest **invisible**
    polynomial: nonzero as a polynomial, vanishing as a function, but
    not coefficientwise ``0`` modulo ``3^k``.
    """
    degree = _require_nat(degree, "degree")
    k = _require_nat(k, "k")
    coeffwise = IntPoly.C(3**k if k else 1)
    invisible: IntPoly | None = None
    if degree >= 3 and k >= 1:
        candidate = parse_scale_x3_minus_x(max(k - 1, 0))
        if candidate.degree <= degree and vanishes_as_function(candidate, k):
            if not coeffwise_vanishes(candidate, k):
                invisible = candidate
        bound = box if box is not None else (2 if k <= 2 else 1)
        best = invisible
        best_score = _score(invisible) if invisible is not None else None
        # Falling-factorial coefficients b_j with 3^k | j! b_j.
        ranges: list[range] = []
        for j in range(degree + 1):
            need = max(k - v3_factorial(j), 0)
            step = 3**need
            limit = step * bound
            ranges.append(range(-limit, limit + 1, step) if step else range(-bound, bound + 1))
        for b in product(*ranges):
            if all(c == 0 for c in b):
                continue
            poly = from_falling(b)
            if poly.degree < 0 or poly.degree > degree:
                continue
            if not vanishes_as_function(poly, k):
                continue
            if coeffwise_vanishes(poly, k):
                continue
            sc = _score(poly)
            if best_score is None or sc < best_score:
                best = poly
                best_score = sc
        invisible = best
    return {
        "degree": degree,
        "k": k,
        "modulus": 3**k if k else 1,
        "coeffwise": coeffwise.render(),
        "coeffwise_coeffs": list(coeffwise.coeffs),
        "invisible": None if invisible is None else invisible.render(),
        "invisible_coeffs": None if invisible is None else list(invisible.coeffs),
        "invisible_newton": None if invisible is None else list(newton_coeffs(invisible)),
        "invisible_monomial_v3": None if invisible is None else valuation_profile(invisible.coeffs),
        "invisible_newton_v3": None if invisible is None else valuation_profile(newton_coeffs(invisible)),
        "factorization": None if invisible is None else _factor_hint(invisible),
    }


def parse_scale_x3_minus_x(scale_val: int) -> IntPoly:
    """``3^{scale_val} (x^3 - x)``."""
    return IntPoly((0, -1, 0, 1)).scale(3**scale_val)


def _factor_hint(poly: IntPoly) -> str:
    if poly.coeffs == (0, -1, 0, 1):
        return "x(x-1)(x+1) = x^3 - x"
    if poly.degree == 3 and poly.coefficient(2) == 0 and poly.coefficient(0) == 0:
        a = poly.coefficient(3)
        c = poly.coefficient(1)
        if a != 0 and c == -a:
            return f"{a}(x^3 - x)"
    if poly.degree == 2 and poly.coefficient(1) == 0 and poly.coefficient(0) == 0:
        return f"{poly.coefficient(2)} x^2"
    if poly.degree >= 1 and all(c == 0 for c in poly.coeffs[:-1]):
        return f"{poly.lc()} x^{poly.degree}"
    return "no short factorization recorded"


def poly_congruence_report(f: IntPoly, g: IntPoly, k: int) -> dict[str, object]:
    """CLI payload for ``btprime calculus poly-congruence``."""
    k = _require_nat(k, "k")
    h = f.sub(g)
    equiv = function_equiv(f, g, k)
    probe = distinguishing_residue(f, g, k)
    tau = first_distinction_horizon(f, g)
    return {
        "f": f.render(),
        "g": g.render(),
        "k": k,
        "modulus": 3**k if k else 1,
        "equivalent": equiv,
        "probe": probe,
        "diff_coeffs": list(h.coeffs),
        "monomial_v3": valuation_profile(h.coeffs),
        "newton": list(newton_coeffs(h)),
        "newton_v3": valuation_profile(newton_coeffs(h)),
        "phi_f": list(pad_phi(phi_k(f, k), max(len(phi_k(f, k)), len(phi_k(g, k))))),
        "phi_g": list(pad_phi(phi_k(g, k), max(len(phi_k(f, k)), len(phi_k(g, k))))),
        "monomial_min_v3": monomial_valuation(h),
        "newton_min_v3": newton_valuation(h),
        "tau": tau,
        "tau_leading_bound": tau_leading_bound(h),
        "coeffwise": coeffwise_vanishes(h, k),
        "candidate_invariant": "Newton residues Δ^j f(0) mod 3^k",
    }


def distinction_row(f: IntPoly, g: IntPoly, word_p=None, word_q=None) -> dict[str, object]:
    """One delayed-distinction record for a residual pair."""
    h = f.sub(g)
    return {
        "p": f.render(),
        "q": g.render(),
        "word_p": None if word_p is None else list(word_p),
        "word_q": None if word_q is None else list(word_q),
        "diff_coeffs": list(h.coeffs),
        "monomial_v3": valuation_profile(h.coeffs),
        "newton": list(newton_coeffs(h)),
        "newton_v3": valuation_profile(newton_coeffs(h)),
        "tau": first_distinction_horizon(f, g),
        "tau_leading_bound": tau_leading_bound(h),
        "monomial_min_v3": monomial_valuation(h),
        "newton_min_v3": newton_valuation(h),
    }


def residual_distinction_dataset(f: IntPoly, k: int, limit: int = 16) -> list[dict[str, object]]:
    """Residual pairs of ``f`` that merge at horizon ``k``, with exact ``τ``."""
    from bt.calculus.myhill_nerode import merge_examples

    rows = []
    for rec in merge_examples(f, k, limit=limit):
        p = _parse_or_skip(rec["p"])
        q = _parse_or_skip(rec["q"])
        if p is None or q is None:
            continue
        row = distinction_row(p, q, rec.get("word_p"), rec.get("word_q"))
        row["split_at_k_plus_1"] = rec.get("split_at_k_plus_1")
        rows.append(row)
    return rows


def _parse_or_skip(text: str) -> IntPoly | None:
    from bt.calculus.section import parse_poly

    try:
        return parse_poly(str(text))
    except (ValueError, TypeError):
        return None


# Stirling numbers of the second kind, used only to document a_j = j! Σ c_i S(i, j).
def stirling2(n: int, k: int) -> int:
    n = _require_nat(n, "n")
    k = _require_nat(k, "k")
    if k > n:
        return 0
    if n == 0:
        return 1 if k == 0 else 0
    table = [0] * (k + 1)
    table[0] = 1
    for i in range(1, n + 1):
        prev = table[0]
        table[0] = 0
        upper = min(i, k)
        for j in range(1, upper + 1):
            cur = table[j]
            table[j] = j * cur + prev
            prev = cur
    return table[k]


def newton_from_monomials(coeffs: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    """``a_j = j! Σ_i c_i S(i, j)`` for LSD-first monomial coefficients."""
    d = len(coeffs) - 1
    if d < 0:
        return (0,)
    out = []
    for j in range(d + 1):
        acc = 0
        for i, c in enumerate(coeffs):
            if c and i >= j:
                acc += c * stirling2(i, j)
        out.append(factorial(j) * acc)
    return tuple(out)
