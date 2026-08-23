"""Phase-0 visibility class of a general ``f ∈ Z[x]``.

After ``D^m(f(p + 3^m x))``, the ``p``-linear monomial of degree ``n≥2``
has valuation ``v_3(n a_n) + m(n-2)``. The candidate law is that some
Newton coordinate sees ``p mod 3^r`` iff that minimum is at most ``k-r``.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product
from math import comb

from bt.calculus.cubic import prefixes_at
from bt.calculus.poly_congruence import newton_coeffs
from bt.calculus.quadratic import iter_dz, pack_word
from bt.calculus.residual import TRITS, residual_along
from bt.calculus.section import IntPoly
from bt.metrics import v3

COEFF_RANGE = (-2, -1, 0, 1, 2)
MAX_DEGREE = 5


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def residual_at_prefix(f: IntPoly, m: int, p: int) -> IntPoly:
    """Closed form of ``D^m(f(p + 3^m x))``."""

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


def min_linear_p_valuation(f: IntPoly, m: int) -> int | None:
    """Minimum ``v_3`` of a ``p``-linear monomial coefficient after ``D^m``."""

    m = _require_nat(m, "m")
    best: int | None = None
    for n in range(2, f.degree + 1):
        a = f.coefficient(n)
        if a == 0:
            continue
        base = v3(a * n)
        if base is None:
            continue
        val = base + m * (n - 2)
        if best is None or val < best:
            best = val
    return best


def cubic_coefficient_unit(f: IntPoly) -> bool:
    """``v_3(a_3)=0``. Exact residue visibility for ``deg f ≤ 3`` at ``r=1``."""

    return f.coefficient(3) % 3 != 0


def predicts_visibility(f: IntPoly, k: int, r: int) -> bool:
    """Degree-``≤3`` law: cubic coefficient invertible mod 3.

    Not a general-degree classifier. Degree 4 contaminates the same
    valuation with a ``p^2`` term; ``x^5`` sees residues via ``p^3≡p``.
    """

    _require_nat(k, "k")
    _require_nat(r, "r")
    return cubic_coefficient_unit(f)


def _visible_iff_residue(values: dict[int, int], r: int, k: int) -> bool:
    mod = 3**k if k else 1
    res_mod = 3**r if r else 1
    n_to_key: dict[int, set[int]] = defaultdict(set)
    key_to_n: dict[int, set[int]] = defaultdict(set)
    for p, val in values.items():
        key = p % res_mod
        residue = val % mod
        n_to_key[residue].add(key)
        key_to_n[key].add(residue)
    return all(len(s) == 1 for s in n_to_key.values()) and all(
        len(s) == 1 for s in key_to_n.values()
    )


def has_visibility(f: IntPoly, k: int, r: int) -> bool:
    k = _require_nat(k, "k")
    r = _require_nat(r, "r")
    m = k - 1 - r
    prefixes = list(prefixes_at(m))
    newtons = {p: newton_coeffs(residual_at_prefix(f, m, p)) for p in prefixes}
    width = max((len(N) for N in newtons.values()), default=1)
    for j in range(width):
        coord = {p: (newtons[p][j] if j < len(newtons[p]) else 0) for p in prefixes}
        if _visible_iff_residue(coord, r, k):
            return True
    return False


def coeff_box(max_degree: int = MAX_DEGREE) -> list[IntPoly]:
    max_degree = _require_nat(max_degree, "max_degree")
    out: list[IntPoly] = []
    for coeffs in product(COEFF_RANGE, repeat=max_degree + 1):
        f = IntPoly(coeffs)
        if f.degree < 0:
            continue
        out.append(f)
    return out


def class_report(k: int = 5, r: int = 1, max_degree: int = MAX_DEGREE) -> dict[str, object]:
    rows = []
    mismatches = []
    for f in coeff_box(max_degree):
        predicted = predicts_visibility(f, k, r)
        actual = has_visibility(f, k, r)
        rec = {"coeffs": f.coeffs, "predicted": predicted, "actual": actual}
        rows.append(rec)
        if predicted != actual:
            mismatches.append(rec)
    return {
        "k": k,
        "r": r,
        "max_degree": max_degree,
        "family_count": len(rows),
        "predicted_true": sum(1 for rec in rows if rec["predicted"]),
        "actual_true": sum(1 for rec in rows if rec["actual"]),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:20],
    }


def formula_matches_residual_along(f: IntPoly, max_m: int = 3) -> bool:
    for m in range(max_m + 1):
        for word in product(TRITS, repeat=m):
            p = pack_word(word)
            if residual_at_prefix(f, m, p) != residual_along(f, word):
                return False
    return True
